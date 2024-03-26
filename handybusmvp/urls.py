from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'user'

urlpatterns = [
    path('', views.index, name='index'),
    path('concert/prereservation/<str:name>/', views.prereservation, name='concertprereservation'),
    path('concert/reservation/<str:name>/', views.concertreservation, name='concertreservation'),
    path('concert/reservationlist/', views.concertreservationlist, name='concertreservationlist'),
    path('concert/prereservationlist/', views.concertprereservationlist, name='concertprereservationlist'),

    path('concert/checkprereservation/', views.checkprereservation, name='checkprereservation'),
    path('concert/checkprereservationinfo/', views.checkprereservationinfo, name='checkprereservationinfo'),
    
    path('concert/checkreservation/', views.checkreservation, name='checkreservation'),
    path('concert/checkreservationinfo/', views.checkreservationinfo, name='checkreservationinfo'),

    path('reservationdone/', views.reservationDone, name='reservationdone'),

    path('prereservationdone/', views.prereservationdone, name='prereservationdone'),

    path('reserverequest/', views.reserverequest, name='reserverequest'),
    path('requestdone/', views.requestdone, name='requestdone'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
