from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User


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
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default= None)

  
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="Guest")
    email = models.EmailField(default="")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    num_tickets = models.PositiveIntegerField(default=1)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"