# Generated by Django 4.1.1 on 2023-06-03 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_productdowload_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='productdowload',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
