from django import forms
from .models import Event
from django_countries import countries

class DateTimeLocalInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class EventForm(forms.ModelForm):
    date_and_time = forms.DateTimeField(input_formats=['%d/%m/%Y, %H:%M'])
    class Meta:
        model = Event
        fields = ['event_type', 'title', 'date_and_time', 'location', 'country', 'description', 'event_image']
        widgets = {
            'date_and_time': DateTimeLocalInput(),
            'country': forms.Select(choices=[(country.code, country.name) for country in countries]),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event_type'].choices = Event.EVENT_TYPE_CHOICES
