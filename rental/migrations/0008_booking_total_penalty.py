# Generated by Django 4.2.11 on 2024-03-29 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0007_alter_booking_booking_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='total_penalty',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
