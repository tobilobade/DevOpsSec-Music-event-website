from django.shortcuts import render,redirect, get_object_or_404
import boto3
from .forms import EventForm, BookingForm
from .models import Event, Booking
from django.contrib.auth.decorators import login_required


def homepage(request):
    upcoming_events = Event.objects.all() # I am getting the objects of the event model
    return render(request, 'events/events_homepage.html', {'upcoming_events': upcoming_events})
    
def upload_to_s3(image_file, file_name):
    s3 = boto3.client('s3')
    bucket_name = 'x23212365-devops-proj'
    s3.upload_fileobj(image_file, bucket_name, file_name)
    return f"https://{bucket_name}.s3.amazonaws.com/{file_name}"

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            # Uploading image to S3
            if 'event_image' in request.FILES:
                s3_url = upload_to_s3(request.FILES['event_image'], request.FILES['event_image'].name)
                event.event_image = s3_url
            event.user=request.user
            event.save()
            return redirect('homepage') 
    else:
        form = EventForm()
    existing_events = Event.objects.filter(user=request.user)
    
    return render(request, 'events/events_submission.html', {'form': form, 'existing_events': existing_events})
    
    
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event-submission') 
    return redirect('homepage') 
    
    
def update_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        # Create a form instance with the POST data and the instance of the house object
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('homepage')  # Redirect to homepage after successful update
    else:
        # If it's a GET request, create a form instance with the instance of the house object
        form = EventForm(instance=event)
    return render(request, 'events/update_event.html', {'form': form})
    
    
def book_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    price_per_ticket = event.price 
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.event_id = event_id
            booking.name = form.cleaned_data['name']  # Assign the name from the form
            booking.save()
            return redirect('my_bookings')  # Redirect to a success page
    else:
        form = BookingForm()
    
    context = {
        'event': event,
        'form': form,
        'price_per_ticket': price_per_ticket,
    }
    
    return render(request, 'events/booking_form.html', context)

def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render (request, "events/my_booking.html", {'bookings': bookings})
    
