from django.db import models
from django.core.validators import FileExtensionValidator
import os
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.timezone import now

def concert_image_path(instance, filename):
    ext = filename.split('.')[-1]
    if isinstance(instance.date, str):
        concert_date = datetime.strptime(instance.date, "%Y-%m-%d").date()
    else:
        concert_date = instance.date
    date_str = concert_date.strftime("%Y%m%d")
    filename = '{}_{}.{}'.format(instance.name, date_str, ext)
    return os.path.join('media/concert_images/', filename)

class Concert(models.Model):    
    name = models.CharField(max_length=255)
    idol = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to=concert_image_path)

class ConcertSchedule(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.PROTECT, related_name='schedules')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = (('concert', 'date'),)
        ordering = ['date', 'start_time']

class Region(models.Model):
    name = models.CharField(max_length=255)

class ConcertRegion(models.Model):
    class Status(models.TextChoices):
        READY_FOR_RESERVATION = 'ready_for_reservation', '예약 준비 단계'
        PRE_RESERVATION = 'pre_reservation', '선예약 모집 단계'
        PRE_RESERVATION_CANCELED = 'pre_reservation_canceled', '선예약 모집 취소'
        PRE_RESERVATION_COMPLETE = 'pre_reservation_complete', '선예약 모집 완료'
        RESERVATION = 'reservation', '실예약 모집 단계'
        RESERVATION_COMPLETE = 'reservation_complete', '실예약 모집 완료'
        RESERVATION_CANCELED = 'reservation_canceled', '실예약 모집 취소'
        BUS_CONTRACT_COMPLETE = 'bus_contract_complete', '버스 대절 완료'
        PAUSED = 'paused', '모집 일시중지 단계'
        CANCELED = 'canceled', '대절 취소'
        FINISHED = 'finished', '콘서트 완료'
    concert_schedule = models.ForeignKey(ConcertSchedule, on_delete=models.PROTECT, related_name='concert_regions')
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name='concert_regions')    
    open_chat_url = models.CharField(max_length=511)
    status = models.CharField(
        max_length=255,
        choices=Status.choices,
        default=Status.READY_FOR_RESERVATION
    )

class Direction(models.TextChoices):
    UPWARD = 'upward', '상행'
    DOWNWARD = 'downward', '하행'

class GatheringPlace(models.Model):
    concert_region = models.ForeignKey(ConcertRegion, on_delete=models.PROTECT, related_name='gathering_places')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True)
    time = models.TimeField(null=True)
    direction = models.CharField(
        max_length=255,
        choices=Direction.choices
    )

class PrivacyConsent(models.Model):
    version = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Pricing(models.Model):
    concert_region = models.ForeignKey(ConcertRegion, on_delete=models.PROTECT, related_name='pricings')
    pre_reserve_price = models.DecimalField(max_digits=10, decimal_places=0)
    round_trip_price = models.DecimalField(max_digits=10, decimal_places=0)
    upbound_price = models.DecimalField(max_digits=10, decimal_places=0)
    downbound_price = models.DecimalField(max_digits=10, decimal_places=0)

class User(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)

class PreReservation(models.Model):
    concert_region = models.ForeignKey(ConcertRegion, on_delete=models.PROTECT, related_name='pre_reservations')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='pre_reservations')
    privacy_consent_version = models.ForeignKey(PrivacyConsent, on_delete=models.PROTECT, null=True, related_name='pre_reservations')

    is_upbound = models.BooleanField()
    is_downbound = models.BooleanField()

    head_count = models.IntegerField(default=1)
    has_paid = models.BooleanField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    refund_account = models.CharField(max_length=255) # 암호화 필요

class Reservation(models.Model):
    concert_region = models.ForeignKey(ConcertRegion, on_delete=models.PROTECT, related_name='reservations')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reservations')
    privacy_consent_version = models.ForeignKey(PrivacyConsent, on_delete=models.PROTECT, null=True, related_name='reservations')  

    gathering_place_up = models.ForeignKey(
        GatheringPlace, 
        on_delete=models.PROTECT, 
        null=True, 
        related_name='upward_reservations'
    )
    gathering_place_down = models.ForeignKey(
        GatheringPlace, 
        on_delete=models.PROTECT, 
        null=True, 
        related_name='downward_reservations'
    )

    head_count = models.IntegerField(default=1)
    has_paid = models.BooleanField()

    preferred_fallback_option = models.CharField(
        max_length=50,
        choices=[
            ('refund', '본인 계좌로 환불'),
            ('pay_extra', '추가금 지불 후 탑승 및 타지역 경유')
        ],
        default='refund',
        verbose_name='인원 미달시 희망하는 진행방향'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_in_charge = models.BooleanField()
    refund_account = models.CharField(max_length=255) # 암호화 필요

class Companion(models.Model):
    pre_reservation = models.ForeignKey(PreReservation, on_delete=models.PROTECT, related_name='companions', null=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.PROTECT, related_name='companions', null=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)

def sns_image_path(instance, filename):
    ext = filename.split('.')[-1]
    reservation = instance.reservation
    user_name = reservation.user.name
    concert_name = reservation.concert_region.concert_schedule.concert.name
    concert_date = reservation.concert_region.concert_schedule.date.strftime("%Y%m%d")
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f'{concert_name}_{concert_date}_{user_name}_{now}.{ext}'
    return os.path.join('media/sns_images', filename)

class EventDiscount(models.Model):
    sns_share_image = models.ImageField(upload_to=sns_image_path, null=True, blank=True)  
    reservation = models.ForeignKey(Reservation, on_delete=models.PROTECT, related_name='event_discounts')
