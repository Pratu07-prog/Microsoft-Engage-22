# Generated by Django 4.0.1 on 2022-05-28 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_movies_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='img',
            field=models.TextField(max_length=300),
        ),
    ]
