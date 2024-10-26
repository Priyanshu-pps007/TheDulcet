# Generated by Django 5.1 on 2024-10-02 03:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_deliverysettings'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='created_at',
            new_name='order_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='dishes',
        ),
        migrations.RemoveField(
            model_name='order',
            name='offers',
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='order_mode',
            field=models.CharField(choices=[('pickup', 'Pickup'), ('delivery', 'Delivery')], default='pickup', max_length=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
