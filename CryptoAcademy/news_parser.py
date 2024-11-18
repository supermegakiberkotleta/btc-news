import os
import openai
import requests
from bs4 import BeautifulSoup
from django.utils.text import slugify
from news.models import News
from django.utils import timezone
from urllib.parse import urljoin
from fake_useragent import UserAgent
from django.conf import settings
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Инициализация OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

def fetch_news():
    base_url = "https://beincrypto.com"
    news_url = urljoin(base_url, "news/")

    ua = UserAgent()  # Инициализируем fake_useragent

    headers = {
        'User-Agent': ua.random  # Используем случайный User-Agent
    }

    for page in range(1, 2):  # Парсим первые 3 страницы
        url = urljoin(news_url, f"page/{page}/")
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch page {page}: {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('div', attrs={'data-el': 'bic-c-news-big'})

        for article in articles:
            link_tag = article.find('a', href=True)
            if not link_tag:
                continue
            detail_url = urljoin(base_url, link_tag['href'])
            parse_detail_page(detail_url, headers)

def translate_text(text, target_language="ru"):
    prompt = f"Translate the following text to {target_language} while preserving its meaning:\n\n{text}"
    print(f"Translation prompt: {prompt}")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Translate the following text to {target_language} while preserving its meaning:"},
            {"role": "user", "content": text}
        ],
        max_tokens=1000
    )
    return response['choices'][0]['message']['content']

def download_image(image_url, slug, headers):
    response = requests.get(image_url, headers=headers)
    if response.status_code == 200:
        image_extension = os.path.splitext(image_url)[1]
        image_path = os.path.join(settings.MEDIA_ROOT, 'news_images', f"{slug}{image_extension}")
        os.makedirs(os.path.dirname(image_path), exist_ok=True)  # Создайте директорию, если она не существует
        with open(image_path, 'wb') as file:
            file.write(response.content)
        return image_path
    return None

def clean_html_content(content, slug, headers):
    soup = BeautifulSoup(content, 'html.parser')
    entry_content = soup.find('div', class_='entry-content-inner')

    if not entry_content:
        return ""

    allowed_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'figure', 'img']

    translated_content_html = ""
    for tag in entry_content.find_all(allowed_tags):
        if tag.name == 'figure':
            img_tag = tag.find('img')
            if img_tag and 'srcset' in img_tag.attrs:
                image_url = img_tag['srcset']
                local_image_path = download_image(image_url, slug, headers)
                if local_image_path:
                    img_tag['src'] = os.path.relpath(local_image_path, settings.MEDIA_ROOT)
                    translated_content_html += str(tag)
        elif tag.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            for a in tag.find_all('a'):
                a.unwrap()  # Remove <a> tags but keep their content
            translated_text = translate_text(tag.get_text(strip=True))
            translated_content_html += f"<{tag.name}>{translated_text}</{tag.name}>"

    print(f"Translated content HTML: {translated_content_html}")
    return translated_content_html

def parse_detail_page(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch detail page: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    title_tag = soup.find('h1')
    if not title_tag:
        print(f"Title not found for URL: {url}")
        return

    title = title_tag.get_text(strip=True)
    translated_title = translate_text(title)

    slug = slugify(title)
    if News.objects.filter(slug=slug).exists():
        return

    content_tag = soup.find('div', class_='entry-content-inner')
    content_html = str(content_tag) if content_tag else ''
    print(f"Original content HTML: {content_html}")

    translated_content_html = clean_html_content(content_html, slug, headers)

    # Скачайте изображение и сохраните его в локальную папку (если необходимо)
    image_path = None
    image_tag = soup.find('div', class_='featured-images')
    if image_tag:
        img = image_tag.find('img')
        if img and 'src' in img.attrs:
            image_url = img['src']
            image_path = download_image(image_url, slug, headers)
            if image_path:
                image_path = os.path.relpath(image_path, settings.MEDIA_ROOT)
    else:
        # Если изображения нет, генерируем его на основе title и content
        generated_image = generate_image(f"News: {title}. {BeautifulSoup(translated_content_html, 'html.parser').get_text()}")
        image_path = os.path.join(settings.MEDIA_ROOT, 'news_images', f"{slug}.png")
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        generated_image.save(image_path)
        image_path = os.path.relpath(image_path, settings.MEDIA_ROOT)

    seo_description = generate_seo_description(translated_title, translated_content_html)
    seo_keywords = generate_seo_keywords(translated_title)

    # Создайте запись в базе данных
    News.objects.create(
        title=translated_title,
        slug=slug,
        content=translated_content_html,
        pub_date=timezone.now(),
        image=image_path,
        seo_title=translated_title,
        seo_description=seo_description,
        seo_keywords=seo_keywords
    )

def generate_seo_description(title, content):
    prompt = f"Generate a concise SEO description for the following content:\n\nTitle: {title}\nContent: {content}"
    print(f"SEO description prompt: {prompt}")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Create a SEO description for the following content."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response['choices'][0]['message']['content']

def generate_seo_keywords(title):
    prompt = f"Generate SEO keywords for the following title:\n\n{title}"
    print(f"SEO keywords prompt: {prompt}")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Create SEO keywords for the following title."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50
    )
    return response['choices'][0]['message']['content']

if __name__ == "__main__":
    fetch_news()
