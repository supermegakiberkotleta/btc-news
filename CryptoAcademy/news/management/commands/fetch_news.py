from django.core.management.base import BaseCommand
import sys
import os

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from news_parser import fetch_news

class Command(BaseCommand):
    help = 'Fetch news from beincrypto.com'

    def handle(self, *args, **kwargs):
        fetch_news()
