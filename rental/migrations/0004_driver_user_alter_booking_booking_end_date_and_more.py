# Generated by Django 4.2.11 on 2024-03-28 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0003_alter_booking_car_alter_booking_customer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_start_date',
            field=models.DateField(),
        ),
    ]
