# Generated by Django 4.1.9 on 2023-07-03 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UWEflix_Website', '0035_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='duration',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Duration'),
        ),
    ]
