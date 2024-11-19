from django.urls import path
from . import views
from .views import NewsListView

urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('<slug:slug>/', views.news_detail, name='news_detail'),
    path('news/new/', views.news_create, name='news_create'),
]
