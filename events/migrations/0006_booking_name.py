# Generated by Django 4.2.11 on 2024-03-12 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_event_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='name',
            field=models.CharField(default='Guest', max_length=100),
        ),
    ]
