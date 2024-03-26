from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import adminviews

app_name = 'admin'

urlpatterns = [
    path('', adminviews.index, name='login'),
    
    path('concert/', adminviews.concert, name='concertadmin'),
    path('concert/addconcert/', adminviews.addconcert, name='addconcert'),
    path('concertInfo/<str:name>/', adminviews.concertInfo, name='concertInfo'),
    path('concert/<int:concert_id>/update_status/', adminviews.updateConcertStatus, name='update_concert_status'),


    
    path('privacyconsent/', adminviews.privacyConsent, name='privacyConsent'),

    path('gatheringplace/<str:name>', adminviews.gatheringPlace, name='gatheringPlace'),
    path('deleteGatheringPlace/<int:place_id>/', adminviews.deleteGatheringPlace, name='deleteGatheringPlace'),
    path('editGatheringPlace/<int:place_id>/', adminviews.editGatheringPlace, name='editGatheringPlace'),

    path('pricing/<str:name>', adminviews.pricing, name='pricing'),
    path('deletePricing/<int:pricing_id>/', adminviews.deletePricing, name='deletePricing'),
    path('editPricing/<int:pricing_id>/', adminviews.editPricing, name='editPricing'),

    path('concert/prereservationstatus/<str:name>/', adminviews.prereservationstatus, name='prereservationstatus'),
    # path('confirm_payment/<int:reservation_id>/', adminviews.confirmPayment, name='confirmpayment'),
    
    path('confirm_reservation_payment/<int:reservation_id>/', adminviews.confirmReservationPayment, name='confirmreservationpayment'),


    path('concert/reservationstatus/<str:name>/', adminviews.reservationstatus, name='reservationstatus'),
    
    path('openchaturl/<str:name>', adminviews.openChatUrl, name='openChatUrl'),
    path('admin/updateConcertRegionStatus/<int:concert_region_id>/', adminviews.updateConcertRegionStatus, name='updateConcertRegionStatus'),

    path('deleteReservation/<int:reservation_id>/', adminviews.deleteReservation, name='deleteReservation'),

    path('leftseat/<str:name>', adminviews.leftseat, name='leftseat'),

    path('concert/confirmrefund/<int:reservation_id>/', adminviews.confirmRefund, name='confirmrefund'),

    path('concert/confirmopenchat/<int:reservation_id>/', adminviews.confirmOpenChat, name='confirmopenchat'),

    path('concert/sendopenchatinvitation/<int:reservation_id>/', adminviews.sendOpenChatInvitation, name='sendopenchatinvitation'),

    path('requestlist/', adminviews.requestlist, name='requestlist'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)