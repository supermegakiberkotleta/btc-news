# Generated by Django 5.1.3 on 2024-11-19 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_alter_news_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='seo_description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='seo_title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
