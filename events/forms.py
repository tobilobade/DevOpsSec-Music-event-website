"""
Module containing forms for event-related functionality.
"""
from datetime import datetime

from django import forms
from django_countries import countries
from django.forms.widgets import DateTimeInput

from .models import Event, Booking

class BookingForm(forms.ModelForm):
    """Form for booking tickets for events."""
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Your Email')
    ticket_type = forms.ChoiceField(choices=[('general', 'General'),
    ('vip', 'VIP')], label='Ticket Type')
    booking_date_time = forms.DateTimeField(widget=forms.HiddenInput(),
    initial=datetime.now)
    num_tickets = forms.IntegerField(initial=1, min_value=1,
    label='Number of Tickets')  # Updated field

    class Meta:
        """fields for booking details."""
        model = Booking
        fields = ['name', 'email', 'num_tickets', 'ticket_type', 'booking_date_time']
    def clean_name(self):
        """
        Clean and validate the 'name' field.
        """
        name = self.cleaned_data.get('name')
        # Placeholder logic: Ensure that the name is at least 3 characters long
        if len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 characters long.")
        return name
    def clean_email(self):
        """
        Clean and validate the 'email' field.
        """
        email = self.cleaned_data.get('email')
        # Placeholder logic: Ensure that the email contains '@'
        if '@' not in email:
            raise forms.ValidationError("Please enter a valid email address.")
        return email


class DateTimeLocalInput(forms.DateTimeInput):
    """Widget for DateTime fields with a local input type."""
    input_type = 'datetime-local'

class EventForm(forms.ModelForm):
    """Form for creating or updating event details."""
    date_and_time = forms.DateTimeField(input_formats=['%d/%m/%Y, %H:%M'],
    widget=DateTimeInput(attrs={'placeholder': 'DD/MM/YYYY, HH:MM'}))
    class Meta:
        """fields for event details."""
        model = Event
        fields = ['event_type', 'title', 'date_and_time', 'location', 'country',
        'description', 'event_image', 'price']
        widgets = {
            'date_and_time': DateTimeLocalInput(),
            'country': forms.Select(choices=[(country.code, country.name)
            for country in countries]),
        }
        
    def clean_date_and_time(self):
        """
        Clean and validate the 'date_and_time' field.
        """
        date_and_time = self.cleaned_data.get('date_and_time')
        # Placeholder logic: Ensure that the event date is in the future
        if date_and_time <= datetime.now():
            raise forms.ValidationError("Event date must be in the future.")
        return date_and_time

    def clean_location(self):
        """
        Clean and validate the 'location' field.
        """
        location = self.cleaned_data.get('location')
        # Placeholder logic: Ensure that the location is not empty
        if not location:
            raise forms.ValidationError("Location cannot be empty.")
        return location
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event_type'].choices = Event.EVENT_TYPE_CHOICES
