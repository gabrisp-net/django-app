# Generated by Django 4.1.1 on 2023-05-13 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uid',
            field=models.CharField(blank=True, max_length=8, unique=True),
        ),
    ]
