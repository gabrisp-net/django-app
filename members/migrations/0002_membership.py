# Generated by Django 4.1.1 on 2023-07-26 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=155)),
                ('description', models.TextField(blank=True)),
                ('id_stripe', models.CharField(blank=True, max_length=100, unique=True)),
                ('price', models.FloatField()),
            ],
        ),
    ]