# Generated by Django 4.2.9 on 2025-03-06 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bizz', '0022_archives_image_url_scraped_data_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='archives',
            name='industry',
        ),
        migrations.RemoveField(
            model_name='archives',
            name='inventory_value',
        ),
        migrations.RemoveField(
            model_name='scraped_data',
            name='industry',
        ),
        migrations.RemoveField(
            model_name='scraped_data',
            name='inventory_value',
        ),
    ]
