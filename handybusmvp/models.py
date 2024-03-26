from django.db import models
from django.core.validators import FileExtensionValidator
import os
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.timezone import now


# Create your models here.

def concert_image_path(instance, filename):
    # 파일 확장자 추출
    ext = filename.split('.')[-1]

    # instance.date가 문자열일 경우 datetime.date 객체로 변환
    if isinstance(instance.date, str):
        # 'YYYY-MM-DD' 형식의 문자열을 datetime.date 객체로 변환
        concert_date = datetime.strptime(instance.date, "%Y-%m-%d").date()
    else:
        concert_date = instance.date

    # 콘서트 날짜를 'YYYYMMDD' 형식으로 변환
    date_str = concert_date.strftime("%Y%m%d")
    filename = '{}_{}.{}'.format(instance.name, date_str, ext)
    return os.path.join('media/concert_images/', filename)

class Concert(models.Model):
    class Status(models.TextChoices):
        READY_FOR_RESERVATION = 'ready_for_reservation', '예약 준비 단계'
        PRE_RESERVATION = 'pre_reservation', '수요조사 모집 단계'
        PRE_RESERVATION_COMPLETE = 'pre_reservation_complete', '수요조사 모집 완료'
        RESERVATION = 'reservation', '예약 모집 단계'
        RESERVATION_COMPLETE = 'reservation_complete', '예약 모집 완료'
        PAUSED = 'paused', '모집 일시중지 단계'
        CANCELED = 'canceled', '대절 취소'
        FINISHED = 'finished', '콘서트 완료'
    
    name = models.CharField(max_length=255)
    idol = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    image = models.ImageField(upload_to=concert_image_path)
    status = models.CharField(
        max_length=255,
        choices=Status.choices,
        default=Status.READY_FOR_RESERVATION
    )
    concert_open_chat_url = models.CharField(max_length=511, null=True, blank=True)

class Region(models.TextChoices):
    DAEGU = 'daegu', '대구'
    DAEJEON = 'daejeon', '대전'
    BUSAN = 'busan', '부산'
    CHANGWON = 'changwon', '창원'
    SEJONG = 'sejong', '세종'
    CHEONGJU = 'cheongju', '청주'
    CHEONAN = 'cheonan', '천안'

        
class ConcertRegionInfo(models.Model):
    class StatusChoices(models.TextChoices):
        BEFORE_CONFIRMATION = 'before_confirmation', '대절 확정 전'
        AFTER_CONFIRMATION = 'after_confirmation', '대절 확정 후'
        CLOSED = 'closed', '마감'
        CANCELLED = 'cancelled', '무산'

    concert = models.ForeignKey(Concert, on_delete=models.PROTECT)
    region = models.CharField(max_length=255, choices=Region.choices)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.BEFORE_CONFIRMATION,
    )
    open_chat_url = models.CharField(max_length=511, null=True, blank=True)
    # TODO: differenciate before confirmation open chat and after confirmation open chat
    # TODO: should consider using multiple buses in one region
    # TODO: 버스 탑승객 선정 알고리즘
    stopover_group = models.IntegerField(null=True, blank=True)

class Direction(models.TextChoices):
        UPWARD = 'upward', '상행'
        DOWNWARD = 'downward', '하행'

class GatheringPlace(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.PROTECT)
    region = models.CharField(
        max_length=255,
        choices=Region.choices
    )
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

class Bus(models.Model):
        concert_region_info = models.ForeignKey(ConcertRegionInfo, on_delete=models.PROTECT)
        capacity = models.IntegerField()
        chat_link = models.CharField(max_length=511)
        status = models.CharField(
            max_length=20,
            choices=ConcertRegionInfo.StatusChoices.choices,
            default=ConcertRegionInfo.StatusChoices.BEFORE_CONFIRMATION
        )

class Pricing(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.PROTECT)
    region = models.CharField(
        max_length=255,
        choices=Region.choices
    )
    pre_reserve_price = models.DecimalField(max_digits=10, decimal_places=0)
    round_trip_price = models.DecimalField(max_digits=10, decimal_places=0)
    upbound_price = models.DecimalField(max_digits=10, decimal_places=0)
    downbound_price = models.DecimalField(max_digits=10, decimal_places=0)

class User(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)

class PreReservation(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    privacy_consent_version = models.ForeignKey(PrivacyConsent, on_delete=models.PROTECT, null=True)

    is_upbound = models.BooleanField()
    is_downbound = models.BooleanField()

    region = models.CharField(
        max_length=255,
        choices=Region.choices
    )
    head_count = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # 업데이트 시간을 올바르게 기록하려면 auto_now=True 사용

class ReservationStatus(models.TextChoices):
        BEFORE_FIXED = 'before_fixed', '대절 확정 전'
        AFTER_FIXED = 'after_fixed', '대절 확정 후'
        CLOSED = 'closed', '마감'
        CANCELLED = 'cancelled', '무산'

class Reservation(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.PROTECT)

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    privacy_consent_version = models.ForeignKey(PrivacyConsent, on_delete=models.PROTECT, null=True)  

    # is_upbound = models.BooleanField()
    # is_downbound = models.BooleanField()

    gathering_place_up = models.ForeignKey(
        GatheringPlace, 
        on_delete=models.PROTECT, 
        null=True, 
        related_name='reservations_up'
    )
    gathering_place_down = models.ForeignKey(
        GatheringPlace, 
        on_delete=models.PROTECT, 
        null=True, 
        related_name='reservations_down'
    )

    head_count = models.IntegerField(default=1)

    has_paid_pre_reserve_price = models.BooleanField()

    has_paid_reserve_price = models.BooleanField()

    funnel = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_in_charge = models.BooleanField()
    refund_account = models.CharField(max_length=255) # 암호화 필요

    status = models.CharField(
        max_length=50,
        choices=ReservationStatus.choices,
        default=ReservationStatus.BEFORE_FIXED,
    )

    has_refunded = models.BooleanField(default=False)
    is_in_open_chat = models.BooleanField(default=False)

    # TODO: 무산시 진행 여부 열 삭제 -> 슬랙에 언급하기

class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        NEED_TO_CHECK = 'need_to_check', '확인 필요'
        COMPLETED = 'completed', '완료'
        FAILED = 'failed', '실패' # 실패 대신에 환불 넣을까 고민중

    pre_reservation = models.ForeignKey(PreReservation, on_delete=models.PROTECT, null=True, blank=True, related_name='pre_payments')
    reservation = models.ForeignKey(Reservation, on_delete=models.PROTECT, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    paid_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=255,
        choices=PaymentStatus.choices,
        default=PaymentStatus.NEED_TO_CHECK
    )


    def clean(self):
        # 둘 중 하나의 예약만 참조하도록 검증
        if (self.pre_reservation is None and self.reservation is None) or (self.pre_reservation and self.reservation):
            raise ValidationError('Specify either a pre_reservation or an actual_reservation, not both.')


class Companion(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='reservation_companions', null=True)
    name = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=50, null=False)

def sns_image_path(instance, filename):
    # 파일 확장자 추출
    ext = filename.split('.')[-1]

    # instance.reservation을 통해 Reservation 인스턴스에 접근
    reservation = instance.reservation
    # reservation.user를 통해 User 인스턴스에 접근하여 사용자 이름을 얻음
    user_name = reservation.user.name

    # reservation.concert를 통해 Concert 인스턴스에 접근하여 콘서트 이름과 날짜를 얻음
    concert_name = reservation.concert.name
    concert_date = reservation.concert.date.strftime("%Y%m%d")

    sns_type_display = instance.get_sns_type_display()

    # 현재 시간을 '년월일시분초' 형태로 변환하여 파일명에 추가
    now = datetime.now().strftime("%Y%m%d%H%M%S")

    # 파일 이름을 '{콘서트 이름}_{콘서트 날짜}_{SNS 타입}_{사용자 이름}_{생성시간}.확장자' 형태로 구성
    filename = f'{concert_name}_{concert_date}_{sns_type_display}_{user_name}_{now}.{ext}'

    # 최종 파일 경로 반환
    return os.path.join('media/sns_images', filename)

class SNS(models.TextChoices):
    TWITTER = 'twitter', '트위터'
    INSTAGRAM = 'instagram', '인스타'

class EventDiscount(models.Model):
    sns_share_image = models.ImageField(
        upload_to=sns_image_path,
        null=True, 
        blank=True
    )  
    sns_type = models.CharField(
        max_length=255,
        choices=SNS.choices
    )
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)

class SurveyCompanion(models.Model):
    pre_reservation = models.ForeignKey(PreReservation, on_delete=models.PROTECT, related_name='survey_companions', null=False)
    name = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=50, null=False)

class ReserveRequest(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    region = models.CharField(max_length=255)
    request_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # TODO: 읽음 처리 기능 vs 수요조사 반영 기능