# Generated by Django 5.0.4 on 2024-04-09 09:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_location', models.CharField(max_length=255)),
                ('dropoff_location', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('REQUESTED', 'Requested'), ('ACCEPTED', 'Accepted'), ('ONGOING', 'Ongoing'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')], default='REQUESTED', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rides_as_driver', to=settings.AUTH_USER_MODEL)),
                ('rider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rides_as_rider', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
