# Generated by Django 5.1 on 2024-10-01 14:42

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_remove_offer_combos_remove_cartitem_combo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='discount_percentage',
        ),
        migrations.AddField(
            model_name='offer',
            name='description',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='offer',
            name='menu',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='order.menu'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='offer',
            name='special_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='offer',
            name='valid_from',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='offer',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]