# Generated by Django 4.2.11 on 2024-03-13 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_alter_booking_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
    ]