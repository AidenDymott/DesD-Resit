# Generated by Django 4.1.9 on 2023-06-23 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UWEflix_Website', '0020_alter_screen_seats'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='screen',
            name='seats',
        ),
    ]
