from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import News
from .forms import NewsForm
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import EmptyPage

def news_list(request):
    news = News.objects.all().order_by('-pub_date')
    return render(request, 'news/news_list.html', {'news': news})

def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug)
    return render(request, 'news/news_detail.html', {'news': news})

def news_create(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.save()
            return redirect('news_detail', pk=news.pk)
    else:
        form = NewsForm()
    return render(request, 'news/news_edit.html', {'form': form})


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'  # Убедитесь, что путь к шаблону корректен
    context_object_name = 'news'  # Имя переменной, используемой в шаблоне
    ordering = ['-pub_date']  # Упорядочение по дате публикации в убывающем порядке
    paginate_by = 15  # Количество новостей на одной странице

def load_more_news(request):
    try:
        if request.method != "GET":
            print("Некорректный метод запроса")
            return JsonResponse({'error': 'Invalid method'}, status=400)

        if request.headers.get('x-requested-with') != 'XMLHttpRequest':
            print("Некорректный заголовок")
            print("Request headers:", request.headers)
            return JsonResponse({'error': 'Invalid headers'}, status=400)

        page = request.GET.get('page')
        if not page or not page.isdigit():
            print("Некорректный параметр page:", page)
            return JsonResponse({'error': 'Invalid page parameter'}, status=400)

        page = int(page)
        news_per_page = 15
        news = News.objects.all().order_by('-pub_date')

        paginator = Paginator(news, news_per_page)
        try:
            news_page = paginator.page(page)
        except EmptyPage:
            print("Страница пуста:", page)
            return JsonResponse({'has_more': False, 'news_html': ''}, status=200)

        news_html = render_to_string('news/partials/news_items.html', {'news': news_page.object_list})

        return JsonResponse({
            'news_html': news_html,
            'has_more': news_page.has_next(),
        }, status=200)

    except Exception as e:
        print("Ошибка в load_more_news:", str(e))
        return JsonResponse({'error': 'Server error'}, status=500)

