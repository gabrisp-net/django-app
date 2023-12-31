# Generated by Django 4.1.1 on 2023-06-24 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_product_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSpecs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, max_length=80)),
                ('value', models.CharField(blank=True, max_length=80)),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]
