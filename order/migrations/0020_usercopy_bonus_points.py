# Generated by Django 5.1 on 2024-10-04 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0019_gallery_remove_offer_dishes_remove_offer_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercopy',
            name='bonus_points',
            field=models.IntegerField(default=0),
        ),
    ]