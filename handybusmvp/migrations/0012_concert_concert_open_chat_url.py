# Generated by Django 4.2 on 2024-03-25 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handybusmvp', '0011_reserverequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='concert',
            name='concert_open_chat_url',
            field=models.CharField(blank=True, max_length=511, null=True),
        ),
    ]
