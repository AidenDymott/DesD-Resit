# Generated by Django 4.1.7 on 2023-06-09 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UWEflix_Website', '0002_movie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='dateShowing',
        ),
    ]
