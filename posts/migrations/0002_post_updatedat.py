# Generated by Django 3.2 on 2023-07-06 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='updatedAt',
            field=models.DateTimeField(auto_now=True),
        ),
    ]