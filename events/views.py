""" file for the view functions"""
from io import BytesIO
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.http import require_POST, require_safe
from django.shortcuts import render,redirect, get_object_or_404
from django.utils import timezone
import qrcode
import boto3
from .forms import EventForm, BookingForm
from .models import Event, Booking


@require_safe
def homepage(request):
    """View function for the homepage."""
    latest_events=Event.objects.filter(
    date_and_time__gte=timezone.now()).order_by('-date_and_time')[:6]
    return render(request, 'events/events_homepage.html', {'latest_events': latest_events})
@require_safe
def all_events(request):
    """View function to view all events."""
    events = Event.objects.all()
    return render(request, 'events/all_events.html', {'events': events})
@require_safe
def search_events(request):
    """View function to search events."""
    query = request.GET.get('query')
    events = Event.objects.filter(
    title__icontains=query) |Event.objects.filter(country__icontains=query)
    return render(request, 'events/search_results.html', {'events': events, 'query': query})
def upload_to_s3(image_file, file_name):
    """Function to upload an image file to AWS S3."""
    s3 = boto3.client('s3')
    bucket_name = 'x23212365-devops-proj'
    s3.upload_fileobj(image_file, bucket_name, file_name)
    return f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
@require_safe
@login_required
def create_event(request):
    """View function for creating an event."""
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            # Uploading image to S3
            if 'event_image' in request.FILES:
                s3_url = upload_to_s3(request.FILES['event_image'],
                request.FILES['event_image'].name)
                event.event_image = s3_url
            event.user=request.user
            event.save()
            return redirect('homepage')
    else:
        form = EventForm()
    existing_events = Event.objects.filter(user=request.user)
    return render(request, 'events/events_submission.html',
    {'form': form, 'existing_events': existing_events})
@require_POST
def delete_event(request, event_id):
    """View function for deleting an event."""
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event-submission')
    return redirect('homepage')
@require_POST
def update_event(request, event_id):
    """View function for updating an event."""
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        # Created a form instance with the POST data and the instance of the house object
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('homepage')  # Redirected to homepage after successful update
    else:
        form = EventForm(instance=event)
    return render(request, 'events/update_event.html', {'form': form})
@require_POST
def book_event(request, event_id):
    """View function for booking an event."""
    event = get_object_or_404(Event, pk=event_id)
    price_per_ticket = event.price
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.event_id = event_id
            booking.name = form.cleaned_data['name']  # Assign the name from the form
            booking.email = form.cleaned_data['email']  # Assign the email from the form
            booking.num_tickets = form.cleaned_data['num_tickets']  # Assign the number of tickets from the form
            booking.save()
            # Generate QR code
            qr_data = f"Name: {booking.name}\nEmail: {booking.email}\nNumber of Tickets: {booking.num_tickets}"
            qr_img = qrcode.make(qr_data)
            qr_img_io = BytesIO()
            qr_img.save(qr_img_io, format='PNG')
            # Send email with QR code
            subject = 'Your Ticket QR Code'
            message = f"Hi {booking.name},\n\nThank you for purchasing tickets to our event. Your booking details are as follows:\n\nName: {booking.name}\nEmail: {booking.email}\nNumber of Tickets: {booking.num_tickets}\n\nPlease find your ticket QR code attached below."
            from_email = 'dammyadetugboboh@gmail.com'  # Replace with your email address
            to_email = booking.email
            email = EmailMultiAlternatives(subject, message, from_email, [to_email])
            email.attach('ticket_qr_code.png', qr_img_io.getvalue(), 'image/png')
            email.send(fail_silently=False)
            return redirect('my_bookings')  # Redirect to a success page
    else:
        form = BookingForm()
    context = {
        'event': event,
        'form': form,
        'price_per_ticket': price_per_ticket,
    }
    return render(request, 'events/booking_form.html', context)
@require_safe
@login_required
def my_bookings(request):
    """View function for viewing bookings of an event."""
    bookings = Booking.objects.filter(user=request.user)
    return render (request, "events/my_booking.html", {'bookings': bookings})
@require_POST
def delete_booking(request, booking_id):
    """View function for deleting bookings of an event."""
    booking = Booking.objects.get(pk=booking_id)
    if request.method == 'POST':
        # Logic for deleting the booking
        booking.delete()
        messages.success(request, 'Booking deleted successfully.')
        return redirect('my_bookings')
    return render(request, 'events/delete_booking_confirmation.html', {'booking': booking})
@require_safe
def contact_us(request):
    """View function for contacting dsaEvents"""
    return render(request, 'events/contact_us.html')
    