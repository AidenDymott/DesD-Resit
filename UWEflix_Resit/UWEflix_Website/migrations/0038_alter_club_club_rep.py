# Generated by Django 4.1.9 on 2023-07-04 18:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UWEflix_Website', '0037_club_delete_clubaccount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='club_rep',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]