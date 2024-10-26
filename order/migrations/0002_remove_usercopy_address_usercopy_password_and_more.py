# Generated by Django 5.1 on 2024-09-24 16:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercopy',
            name='address',
        ),
        migrations.AddField(
            model_name='usercopy',
            name='password',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='usercopy',
            name='username',
            field=models.CharField(default=0, max_length=25, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usercopy',
            name='phone_number',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='usercopy',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
