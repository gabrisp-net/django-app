# Generated by Django 4.1.1 on 2023-05-02 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_stripe_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='stripe_id',
            field=models.CharField(max_length=200),
        ),
    ]
