# Generated by Django 4.0.1 on 2022-01-28 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_rename_vechicle_type_ride_vehicle_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='has_shared',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ride',
            name='owner_number',
            field=models.IntegerField(default=0),
        ),
    ]
