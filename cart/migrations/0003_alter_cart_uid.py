# Generated by Django 4.1.1 on 2023-04-30 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_alter_cart_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='uid',
            field=models.CharField(default='FA745', editable=False, max_length=50, unique=True),
        ),
    ]