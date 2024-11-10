from django.contrib import admin
from .models import News

class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'pub_date', 'seo_title', 'seo_description', 'seo_keywords')
    fields = ('title', 'slug', 'content', 'pub_date', 'image', 'seo_title', 'seo_description', 'seo_keywords')

admin.site.register(News, NewsAdmin)
