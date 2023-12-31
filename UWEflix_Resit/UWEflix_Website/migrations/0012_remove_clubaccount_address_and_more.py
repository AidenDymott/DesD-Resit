# Generated by Django 4.1.7 on 2023-06-15 19:22

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('UWEflix_Website', '0011_alter_screen_seats'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clubaccount',
            name='address',
        ),
        migrations.RemoveField(
            model_name='clubaccount',
            name='contact',
        ),
        migrations.AddField(
            model_name='clubaccount',
            name='city',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='clubaccount',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='clubaccount',
            name='landline',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='clubaccount',
            name='mobile',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='clubaccount',
            name='post_code',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='clubaccount',
            name='street',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='clubaccount',
            name='street_number',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='clubaccount',
            name='account_ID',
            field=models.UUIDField(blank=True, unique=True, verbose_name=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='showing',
            name='date_showing',
            field=models.DateField(verbose_name='Movie Showing Date'),
        ),
        migrations.AlterField(
            model_name='showing',
            name='time_showing',
            field=models.TimeField(verbose_name='Movie Showing Time'),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
    ]
