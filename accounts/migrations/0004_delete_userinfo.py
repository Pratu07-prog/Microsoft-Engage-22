# Generated by Django 4.0.1 on 2022-05-26 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_user_userinfo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='userinfo',
        ),
    ]
