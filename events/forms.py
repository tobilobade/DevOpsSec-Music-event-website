from django import forms
from .models import Event, Booking
from django_countries import countries
from datetime import datetime
from django.forms.widgets import DateTimeInput

class BookingForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Your Email') 
    ticket_type = forms.ChoiceField(choices=[('general', 'General'), ('vip', 'VIP')], label='Ticket Type')
    booking_date_time = forms.DateTimeField(widget=forms.HiddenInput(), initial=datetime.now)
    num_tickets = forms.IntegerField(initial=1, min_value=1, label='Number of Tickets')  # Updated field

    class Meta:
        model = Booking
        fields = ['name', 'email', 'num_tickets', 'ticket_type', 'booking_date_time']


class DateTimeLocalInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class EventForm(forms.ModelForm):
    date_and_time = forms.DateTimeField(input_formats=['%d/%m/%Y, %H:%M'], widget=DateTimeInput(attrs={'placeholder': 'DD/MM/YYYY, HH:MM'}))
    class Meta:
        model = Event
        fields = ['event_type', 'title', 'date_and_time', 'location', 'country', 'description', 'event_image', 'price']
        widgets = {
            'date_and_time': DateTimeLocalInput(),
            'country': forms.Select(choices=[(country.code, country.name) for country in countries]),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event_type'].choices = Event.EVENT_TYPE_CHOICES
