# Generated by Django 4.1.9 on 2023-07-04 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UWEflix_Website', '0036_alter_movie_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('club_name', models.CharField(max_length=200)),
                ('landline', models.CharField(blank=True, max_length=20)),
                ('mobile', models.CharField(blank=True, max_length=20)),
                ('street_number', models.CharField(blank=True, max_length=50)),
                ('street', models.CharField(blank=True, max_length=200)),
                ('city', models.CharField(blank=True, max_length=200)),
                ('post_code', models.CharField(blank=True, max_length=20)),
                ('club_rep', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='ClubAccount',
        ),
    ]
