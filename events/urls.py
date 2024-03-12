from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
 
urlpatterns = [
 path('', views.homepage, name='homepage'),
 path('events-submission/', views.create_event, name='event-submission'),
 path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
 path('update/<int:event_id>/', views.update_event, name='update_event'),
 path('book/<int:event_id>/', views.book_event, name='book_event'),
 path('my-bookings/', views.my_bookings, name='my_bookings'),
 
]

urlpatterns += staticfiles_urlpatterns()