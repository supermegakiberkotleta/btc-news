from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import News
from .forms import NewsForm
from django.views.generic import ListView

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
    template_name = 'news_list.html'  # замените на имя вашего шаблона
    context_object_name = 'news'
    ordering = ['-pub_date']  # сортировка по дате публикации в убывающем порядке

