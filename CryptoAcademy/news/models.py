from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = RichTextField()  # Используем RichTextField для поддержки WYSIWYG-редактора
    pub_date = models.DateTimeField('date published')
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    seo_title = models.CharField(max_length=60, blank=True, null=True)
    seo_description = models.CharField(max_length=160, blank=True, null=True)
    seo_keywords = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

