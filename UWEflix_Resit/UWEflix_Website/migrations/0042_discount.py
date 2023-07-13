# Generated by Django 4.1.9 on 2023-07-13 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UWEflix_Website', '0041_alter_booking_total_cost'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20, unique=True)),
                ('perc', models.PositiveIntegerField()),
            ],
        ),
    ]