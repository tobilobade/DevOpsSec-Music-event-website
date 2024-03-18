"""url definitions for the routes"""
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
urlpatterns = [
 path('', views.homepage, name='homepage'),
 path('events-submission/', views.create_event, name='event-submission'),
 path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
 path('update/<int:event_id>/', views.update_event, name='update_event'),
 path('book/<int:event_id>/', views.book_event, name='book_event'),
 path('my-bookings/', views.my_bookings, name='my_bookings'),
 path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
 path('all-events/', views.all_events, name='all_events'),
 path('search/', views.search_events, name='search_events'),
 path('contact-us/', views.contact_us, name='contact_us'),
]
urlpatterns += staticfiles_urlpatterns()
