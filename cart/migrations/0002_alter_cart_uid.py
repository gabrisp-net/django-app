# Generated by Django 4.1.1 on 2023-04-30 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='uid',
            field=models.CharField(default='A7DA7', editable=False, max_length=50),
        ),
    ]