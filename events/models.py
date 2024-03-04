from django.db import models
from django_countries.fields import CountryField

class Event(models.Model):
    EVENT_TYPE_CHOICES = (
        ('concert', 'Concert'),
        ('music_festival', 'Music Festival'),
        ('workshop', 'Workshop'),
        ('conference', 'Conference'),
        ('exhibition', 'Exhibition'),
        ('album_release', 'Album Release'),
        ('live_stream', 'Live Stream'),
        ('meetup', 'Meetup'),
    )
    
    event_type = models.CharField(max_length=100, choices=EVENT_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    date_and_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    country = CountryField()
    description = models.TextField()
    event_image = models.ImageField(blank=True)

  
