# Generated by Django 4.2 on 2024-03-20 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handybusmvp', '0008_concertregioninfo_stopover_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='had_refunded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reservation',
            name='is_in_open_chat',
            field=models.BooleanField(default=False),
        ),
    ]
