from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
 
urlpatterns = [
 path('', views.homepage, name='homepage'),
 path('events-submission/', views.create_event, name='event-submission'),
 path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
]

urlpatterns += staticfiles_urlpatterns()