# Generated by Django 4.1.1 on 2023-07-26 22:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_itemmembership_preview_productmembership_preview_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='billing',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
