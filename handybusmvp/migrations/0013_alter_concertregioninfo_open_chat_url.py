# Generated by Django 4.2 on 2024-03-25 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handybusmvp', '0012_concert_concert_open_chat_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concertregioninfo',
            name='open_chat_url',
            field=models.CharField(blank=True, max_length=511, null=True),
        ),
    ]