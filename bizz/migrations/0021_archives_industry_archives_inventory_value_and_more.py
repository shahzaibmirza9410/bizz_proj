# Generated by Django 4.2.9 on 2025-02-17 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bizz', '0020_alter_list_filters_alter_list_user_filters'),
    ]

    operations = [
        migrations.AddField(
            model_name='archives',
            name='industry',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='archives',
            name='inventory_value',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='archives',
            name='listing_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='scraped_data',
            name='industry',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='scraped_data',
            name='inventory_value',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='scraped_data',
            name='listing_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
