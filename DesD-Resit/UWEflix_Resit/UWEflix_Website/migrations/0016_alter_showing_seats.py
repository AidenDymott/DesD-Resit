# Generated by Django 4.1.9 on 2023-06-16 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UWEflix_Website', '0015_showing_screen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='showing',
            name='seats',
            field=models.PositiveIntegerField(),
        ),
    ]
