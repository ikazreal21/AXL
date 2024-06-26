# Generated by Django 4.2.11 on 2024-03-28 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0002_alter_cars_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='car',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rental.cars'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rental.customer'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rental.driver'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_customer',
            field=models.BooleanField(default=True, verbose_name='Customer'),
        ),
    ]
