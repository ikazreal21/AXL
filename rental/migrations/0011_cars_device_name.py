# Generated by Django 4.2.11 on 2024-03-29 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0010_customer_is_first_time_driver_is_first_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='cars',
            name='device_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
