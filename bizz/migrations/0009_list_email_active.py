# Generated by Django 4.2.9 on 2024-09-28 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bizz', '0008_remove_list_email_frequecy_list_email_frequency'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='email_active',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
