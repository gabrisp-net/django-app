# Generated by Django 4.1.1 on 2023-06-26 21:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_productspecs'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='comingsoon',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='date',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
