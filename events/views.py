from django.shortcuts import render,redirect, get_object_or_404
import boto3
from .forms import EventForm
from .models import Event

def homepage(request):
    upcoming_events = Event.objects.all() # getting the objects of the event model
    return render(request, 'events/events_homepage.html', {'upcoming_events': upcoming_events})
    
def upload_to_s3(image_file, file_name):
    s3 = boto3.client('s3')
    bucket_name = 'x23212365-devops-proj'
    s3.upload_fileobj(image_file, bucket_name, file_name)
    return f"https://{bucket_name}.s3.amazonaws.com/{file_name}"

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            # Upload image to S3
            if 'event_image' in request.FILES:
                s3_url = upload_to_s3(request.FILES['event_image'], request.FILES['event_image'].name)
                event.event_image = s3_url
            event.save()
            return redirect('homepage')  # Redirect to the home page after successfully creating an event
    else:
        form = EventForm()
    existing_events = Event.objects.all()
    
    return render(request, 'events/events_submission.html', {'form': form, 'existing_events': existing_events})
    
    
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event-submission')  # Redirect to the homepage or any other appropriate URL
    return redirect('homepage') 