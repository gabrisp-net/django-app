# Generated by Django 4.1.1 on 2023-06-03 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_product_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='line',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
