# Generated by Django 4.0.1 on 2022-05-24 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.TextField(null=True)),
                ('user_genre', models.TextField(max_length=250)),
                ('user_actor', models.TextField(max_length=250)),
                ('user_actress', models.TextField(max_length=250)),
            ],
        ),
    ]