from django.shortcuts import redirect, render, get_list_or_404
from django.urls import reverse
from .models import Concert, PrivacyConsent, GatheringPlace, Pricing, Region, Direction, PreReservation, Reservation, EventDiscount, ConcertRegionInfo, SNS, ReservationStatus, ReserveRequest
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.conf import settings
import os
from datetime import datetime
from django.db.models import Count
from collections import defaultdict
from django.db.models import Case, When, Value, DecimalField, Exists, OuterRef, Subquery, F, IntegerField, Sum
import requests
from dotenv import load_dotenv
from django.contrib import messages
from .functions import change_name, getStopOver, getRidingInfoAndReservationStatus
# Create your views here.

# 콘서트 별 현황 통해서 예약 페이지 제작 가능 등등 로직 설정하기


def index(request):
    context = {}
    if request.method == 'POST':
        # 로그인 폼으로부터 'username'과 'password'를 받아옵니다.
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # authenticate 함수를 사용하여 사용자 인증을 시도합니다.
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # 사용자가 존재하고 비밀번호가 맞다면 로그인 처리를 합니다.
            login(request, user)
            # 성공적으로 로그인 처리 후 리디렉션할 페이지로 이동합니다.
            return redirect('admin:concertadmin')
        else:
            # 인증 실패 시, 로그인 폼으로 다시 리디렉션하고 오류 메시지를 표시할 수 있습니다.
            return render(request, 'handybusmvp/admin/index.html', {'error': 'Invalid username or password'})
    else:

        return render(request, 'handybusmvp/admin/index.html', context)

@login_required
def concert(request):
    concert_groups = Concert.objects.values('name').annotate(date_count=Count('date')).order_by('name')

    concert_data = []
    for group in concert_groups:
        concerts = Concert.objects.filter(name=group['name']).order_by('date')

        concert_data.append({
            'name': group['name'],
            'concerts': list(concerts)  # 날짜, 상태, 이미지를 저장
        })

    context = {'concert_data': concert_data}
    return render(request, 'handybusmvp/admin/concertadmin.html', context)


@login_required
def concertInfo(request, name):
    concerts = Concert.objects.filter(name=name).order_by('date')

    concert_info = []
    for concert in concerts:
        upward_places = GatheringPlace.objects.filter(concert=concert, direction=Direction.UPWARD).order_by('region', 'time')
        downward_places = GatheringPlace.objects.filter(concert=concert, direction=Direction.DOWNWARD).order_by('region', 'time')
        pricing_info = Pricing.objects.filter(concert=concert).order_by('region')
        open_chat_urls = ConcertRegionInfo.objects.filter(concert=concert).order_by('region')

        concert_info.append({
            'concert': concert,
            'upward_places': upward_places,
            'downward_places': downward_places,
            'pricing_info': pricing_info,
            'open_chat_urls': open_chat_urls  # 오픈채팅방 URL 정보를 포함
        })

    context = {
        'concert_info': concert_info,
        'name': name
    }
    return render(request, 'handybusmvp/admin/concertinfo.html', context)



@login_required
@require_POST
def updateConcertStatus(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)
    status = request.POST.get('status')
    if status in dict(Concert.Status.choices).keys():
        concert.status = status
        concert.save()
    return redirect('admin:concertInfo', name=concert.name)

@csrf_protect
@login_required
def addconcert(request):
    upcoming_concerts = Concert.objects.filter(date__gte=timezone.now().date())
    selected_concert = None

    if request.method == 'GET' and 'concert_id' in request.GET:
        concert_id = request.GET.get('concert_id')
        selected_concert = get_object_or_404(Concert, pk=concert_id)

    if request.method == 'POST':
        # Form 데이터 받기
        name = request.POST.get('name')
        idol = request.POST.get('idol')
        date = request.POST.get('date')
        location = request.POST.get('location')
        start_time = request.POST.get('starttime')
        end_time = request.POST.get('endtime', None)
        image = request.FILES.get('image')  # 파일 객체
        concert_open_chat = request.POST.get('concert_open_chat')

        # 빈 문자열이면 None으로 설정
        if end_time == "":
            end_time = None

        # Concert 객체 생성 및 저장
        concert = Concert(
            name=name,
            idol=idol,
            date=date,
            location=location,
            start_time=start_time,
            end_time=end_time,
            image=image,
            concert_open_chat = concert_open_chat  # 파일 객체 직접 할당
            # 여기서 status 필드 값 할당 필요 (여기서 생략)
        )
        concert.save()

        # TODO: add default values of gathering places, pricings

        return redirect('admin:concertadmin')

    context = {
        'upcoming_concerts': upcoming_concerts,
        'selected_concert': selected_concert
    }

    return render(request, 'handybusmvp/admin/addconcert.html', context)

@login_required
def privacyConsent(request):
    if request.method == 'POST':
        version = request.POST.get('version')
        content = request.POST.get('content')
        PrivacyConsent.objects.create(version=version, content=content)
        return redirect('admin:privacyConsent')

    privacyConsents = PrivacyConsent.objects.all()
    context = {'privacyConsents': privacyConsents}
    return render(request, 'handybusmvp/admin/privacyconsent.html', context)

@login_required
def gatheringPlace(request, name):
    concerts = Concert.objects.filter(name=name).order_by('date')
    concert_places = []

    for concert in concerts:
        upward_places = GatheringPlace.objects.filter(concert=concert, direction=Direction.UPWARD).order_by('region', 'time')
        downward_places = GatheringPlace.objects.filter(concert=concert, direction=Direction.DOWNWARD).order_by('region', 'time')
        concert_places.append((concert, upward_places, downward_places))

    if request.method == 'POST':
        # Extracting data from POST request
        region = request.POST.get('region')
        place_name = request.POST.get('name')  # Avoid conflict with 'name' variable in function
        location = request.POST.get('location')
        time = request.POST.get('time', None)
        if time == "":  # 빈 문자열이면 None으로 설정
            time = None
        concert_id = request.POST.get('concert_id')  # Need to pass concert_id in the form
        direction = request.POST.get('direction')

        # Getting the corresponding concert
        concert = Concert.objects.get(id=concert_id)

        # Creating a new gathering place
        new_place = GatheringPlace.objects.create(concert=concert, region=region, name=place_name, location=location, time=time, direction=direction)


        # Redirect to refresh the page and see the new gathering place
        return redirect('admin:gatheringPlace', name=name)

    regions = [(region.value, region.label) for region in Region]
    directions = Direction.choices


    context = {
        'concert_places': concert_places,
        'name': name,
        'regions': regions,
        'directions': directions,
    }


    return render(request, 'handybusmvp/admin/gatheringplace.html', context)

@login_required
def editGatheringPlace(request, place_id):
    place = get_object_or_404(GatheringPlace, id=place_id)
    if request.method == 'POST':
        place.name = request.POST.get('name')
        place.location = request.POST.get('location')
        place.time = request.POST.get('time')
        place.save()
        return redirect('admin:gatheringPlace', name=place.concert.name)

@login_required
def deleteGatheringPlace(request, place_id):
    place = get_object_or_404(GatheringPlace, id=place_id)
    concert_name = place.concert.name  # GatheringPlace와 연결된 Concert의 이름을 가져옵니다.
    place.delete()
    return redirect('admin:gatheringPlace', name=concert_name)  # Concert 이름을 파라미터로 전달하여 리디렉션

@login_required
def pricing(request, name):
    concerts = Concert.objects.filter(name=name).order_by('date')
    pricingEntries = []

    for concert in concerts:
        prices = Pricing.objects.filter(concert=concert).order_by('region')
        for price in prices:
            pricingEntries.append((concert, price))

    if request.method == 'POST':
        # Extracting data from POST request
        region = request.POST.get('region')
        pre_reserve_price = request.POST.get('pre_reserve_price')
        round_trip_price = request.POST.get('round_trip_price')
        upbound_price = request.POST.get('upbound_price')
        downbound_price = request.POST.get('downbound_price')
        concert_id = request.POST.get('concert_id')

        # Getting the corresponding concert
        concert = Concert.objects.get(id=concert_id)

        # Creating a new pricing entry
        new_price = Pricing(
            concert=concert,
            region=region,
            pre_reserve_price=pre_reserve_price,
            round_trip_price=round_trip_price,
            upbound_price=upbound_price,
            downbound_price=downbound_price
        )
        new_price.save()

        # Redirect to refresh the page and see the new pricing entry
        return redirect('admin:pricing', name=name)

    context = {
        'concerts': concerts,
        'pricingEntries': pricingEntries,
        'name': name,
        'regions': Region.choices,  # Region.choices 추가

    }

    return render(request, 'handybusmvp/admin/pricing.html', context)

@login_required
def deletePricing(request, pricing_id):
    pricing = get_object_or_404(Pricing, id=pricing_id)
    pricing.delete()
    return redirect('admin:pricing', name=pricing.concert.name)

@login_required
def editPricing(request, pricing_id):
    pricing = get_object_or_404(Pricing, id=pricing_id)
    if request.method == 'POST':
        pricing.pre_reserve_price = request.POST.get('pre_reserve_price')
        pricing.round_trip_price = request.POST.get('round_trip_price')
        pricing.upbound_price = request.POST.get('upbound_price')
        pricing.downbound_price = request.POST.get('downbound_price')
        pricing.save()
        return redirect('admin:pricing', name=pricing.concert.name)

@login_required
def prereservationstatus(request, name):
    concerts = Concert.objects.filter(name=name).order_by('date')
    reservations_list = []
    regions_dict = {region_code: label for region_code, label in Region.choices}

    for concert in concerts:
        reservations = PreReservation.objects.filter(concert=concert)\
                                            .select_related('user')\
                                            .prefetch_related('survey_companions')\
                                            .order_by('created_at')


        region_up_down_counts = {region_code: {'upbound': 0, 'downbound': 0} for region_code in regions_dict}

        for reservation in reservations:
            region_code = reservation.region
            if region_code in regions_dict:
                if reservation.is_upbound:
                    region_up_down_counts[region_code]['upbound'] += reservation.head_count
                if reservation.is_downbound:
                    region_up_down_counts[region_code]['downbound'] += reservation.head_count

                # Determine travel type based on is_upbound and is_downbound flags
                reservation.travel_type = '왕복' if reservation.is_upbound and reservation.is_downbound else '상행' if reservation.is_upbound else '하행' if reservation.is_downbound else '정보 없음'
                
                companions = reservation.survey_companions.all()
                reservation.companions_list = ', '.join([f"{companion.name} ({companion.phone_number})" for companion in companions])
            else:
                print(f"오류: '{region_code}' 지역 코드는 Region.choices에 정의되지 않았습니다.")

        region_counts_list = [{
            'region_name': regions_dict[region_code],
            'upbound': counts['upbound'],
            'downbound': counts['downbound']
        } for region_code, counts in region_up_down_counts.items()]

        reservations_list.append({
            'concert': concert,
            'reservations': reservations,
            'region_counts_list': region_counts_list
        })

    return render(request, 'handybusmvp/admin/prereservation.html', {
        'reservations_list': reservations_list,
        'regions': regions_dict
    })

@login_required
def reservationstatus(request, name):
    concerts = Concert.objects.filter(name=name).order_by('date')
    reservations_list = []



    for concert in concerts:
        # 지역별 및 집합장소별 인원 현황을 저장할 딕셔너리 초기화
        regions_dict = {region_code: {'upbound': 0, 'downbound': 0} for region_code, region_name in Region.choices}
        gathering_place_dict = {}

        reservations = Reservation.objects.filter(concert=concert)\
            .select_related('user', 'gathering_place_up', 'gathering_place_down')\
            .prefetch_related('reservation_companions', 'eventdiscount_set')\
            .annotate(
                up_region=F('gathering_place_up__region'),
                down_region=F('gathering_place_down__region'),
                up_exists=Exists(GatheringPlace.objects.filter(id=OuterRef('gathering_place_up_id'))),
                down_exists=Exists(GatheringPlace.objects.filter(id=OuterRef('gathering_place_down_id'))),
                twitter_discount_exists=Exists(EventDiscount.objects.filter(reservation=OuterRef('pk'), sns_type=SNS.TWITTER)),
                instagram_discount_exists=Exists(EventDiscount.objects.filter(reservation=OuterRef('pk'), sns_type=SNS.INSTAGRAM)),
            ).annotate(
                pre_reserve_deposit=Case(
                    When(up_exists=True, then=Subquery(
                        Pricing.objects.filter(
                            concert=concert,
                            region=OuterRef('up_region')
                        ).values('pre_reserve_price')[:1]
                    ) * F('head_count')),
                    When(down_exists=True, then=Subquery(
                        Pricing.objects.filter(
                            concert=concert,
                            region=OuterRef('down_region')
                        ).values('pre_reserve_price')[:1]
                    ) * F('head_count')),
                    default=Value(0),
                    output_field=DecimalField()
                ),
                trip_price=Case(
                    When(up_exists=True, down_exists=True, then=Subquery(
                        Pricing.objects.filter(
                            concert=concert,
                            region=OuterRef('up_region')
                        ).values('round_trip_price')[:1]
                    )),
                    When(up_exists=True, down_exists=False, then=Subquery(
                        Pricing.objects.filter(
                            concert=concert,
                            region=OuterRef('up_region')
                        ).values('upbound_price')[:1]
                    )),
                    When(up_exists=False, down_exists=True, then=Subquery(
                        Pricing.objects.filter(
                            concert=concert,
                            region=OuterRef('down_region')
                        ).values('downbound_price')[:1]
                    )),
                    default=Value(0),
                    output_field=DecimalField()
                ) * F('head_count')
            ).annotate(
                discount_amount=Case(
                    When(twitter_discount_exists=True, instagram_discount_exists=True, then=Value(2000)),
                    When(twitter_discount_exists=True, then=Value(1000)),
                    When(instagram_discount_exists=True, then=Value(1000)),
                    default=Value(0),
                    output_field=DecimalField()
                )
            ).annotate(
                required_deposit=Case(
                    When(status=ReservationStatus.BEFORE_FIXED, then=F('trip_price') - F('discount_amount') - F('pre_reserve_deposit')),
                    When(status=ReservationStatus.AFTER_FIXED, then=F('trip_price') - F('discount_amount')),
                    default=F('trip_price') - F('discount_amount'), # Other status cases
                    output_field=DecimalField()
                )
            ).order_by('created_at')


        # 지역별 및 집합장소별 인원 집계 로직
        for reservation in reservations:

            if reservation.up_exists and reservation.down_exists:
                reservation.travel_type = '왕복'
            elif reservation.up_exists:
                reservation.travel_type = '상행'
            elif reservation.down_exists:
                reservation.travel_type = '하행'
            else:
                reservation.travel_type = '정보 없음'  # 상행/하행 정보가 없는 경우

            if reservation.gathering_place_up:
                up_region = reservation.gathering_place_up.region
                up_place_name = reservation.gathering_place_up.name

                # Ensure the region is initialized in regions_dict (it should be already, but this is just for safety)
                regions_dict.setdefault(up_region, {'upbound': 0, 'downbound': 0})
                regions_dict[up_region]['upbound'] += reservation.head_count

                # Initialize and update the gathering place counts
                gathering_place_dict.setdefault(up_place_name, {'upbound': 0, 'downbound': 0})
                gathering_place_dict[up_place_name]['upbound'] += reservation.head_count

            if reservation.gathering_place_down:
                down_region = reservation.gathering_place_down.region
                down_place_name = reservation.gathering_place_down.name

                # Ensure the region is initialized in regions_dict
                regions_dict.setdefault(down_region, {'upbound': 0, 'downbound': 0})
                regions_dict[down_region]['downbound'] += reservation.head_count

                # Initialize and update the gathering place counts
                gathering_place_dict.setdefault(down_place_name, {'upbound': 0, 'downbound': 0})
                gathering_place_dict[down_place_name]['downbound'] += reservation.head_count

            # 동승인 정보 처리
            companions = reservation.reservation_companions.all()
            reservation.companions_list = ', '.join([f"{companion.name} ({companion.phone_number})" for companion in companions])

            # 할인 이미지 처리
            # Initialize attributes for Twitter and Instagram images
            reservation.twitter_image_url = None
            reservation.instagram_image_url = None

            # Iterate over all event discounts associated with this reservation
            for event_discount in reservation.eventdiscount_set.all():
                if event_discount.sns_type == SNS.TWITTER:
                    reservation.twitter_image_url = event_discount.sns_share_image.url if event_discount.sns_share_image else None
                elif event_discount.sns_type == SNS.INSTAGRAM:
                    reservation.instagram_image_url = event_discount.sns_share_image.url if event_discount.sns_share_image else None
            
            # Fetch the ConcertRegionInfo for the reservation's up and down regions, if they exist
            if reservation.gathering_place_up:
                region_info = ConcertRegionInfo.objects.filter(concert=concert, region=reservation.gathering_place_up.region).last()
                reservation.region_status = region_info.status if region_info else None
            if reservation.down_exists:
                region_info = ConcertRegionInfo.objects.filter(concert=concert, region=reservation.gathering_place_down.region).last()
                reservation.region_status = region_info.status if region_info else ConcertRegionInfo.StatusChoices.BEFORE_CONFIRMATION


        # 지역별 및 집합장소별 인원 현황을 리스트로 변환하여 reservations_list에 추가
        # Region.choices에서 코드에 대응하는 이름(레이블)을 찾는 딕셔너리 생성
        region_display_dict = dict(Region.choices)

        # 지역별 및 집합장소별 인원 현황을 리스트로 변환하여 reservations_list에 추가
        region_counts_list = [{
            'region_name': region_display_dict.get(k, '알 수 없음'),  # 지역 코드 대신 레이블 사용
            **v
        } for k, v in regions_dict.items()]


        gathering_place_counts_list = [{'gathering_place_name': k, **v} for k, v in gathering_place_dict.items()]

        reservations_list.append({
            'concert': concert,
            'reservations': reservations,
            'region_counts_list': region_counts_list,
            'gathering_place_counts_list': gathering_place_counts_list,
        })

    return render(request, 'handybusmvp/admin/reservation.html', {
        'reservations_list': reservations_list,
    })

# @require_POST
# def confirmPayment(request, reservation_id):
#     reservation = get_object_or_404(PreReservation, pk=reservation_id)
#     reservation.has_paid = True
#     reservation.save()

#     send_pre_reservation_confirmed_message(phone_num=reservation.user.phone_number.replace("-",""), name=reservation.user.name, concert_name=reservation.concert.name, concert_date=reservation.concert.date)
    
#     # 선예약 예약 현황 페이지로 리다이렉트합니다. 여기서는 콘서트 이름을 사용합니다.
#     return redirect('admin:prereservationstatus', name=reservation.concert.name)

def send_pre_reservation_confirmed_message(phone_num, name, concert_name, concert_date):
    load_dotenv(os.path.join(os.path.dirname(__file__), '../', 'env'))

    api_key = os.getenv('MESSAGE_API_KEY')
    id_key = os.getenv('MESSAGE_ID')

    send_url = 'https://apis.aligo.in/send/' # 요청을 던지는 URL, 현재는 문자보내기
    sms_data={'key': api_key, #api key
        'userid': id_key, # 알리고 사이트 아이디
        'sender': '01085146141', # 발신번호
        'receiver': phone_num, # 수신번호 (,활용하여 1000명까지 추가 가능)
        'msg': f'%고객명%님 {concert_name}({concert_date}) 버스 대절 가신청이 완료되었습니다.\n\n이후에 잔금 납입 문자로 추가 안내드릴 예정입니다.\n\n감사합니다.', #문자 내용 
        'msg_type' : 'LMS', #메세지 타입 (SMS, LMS)
        'title' : 'Handybus 가신청 확인 안내', #메세지 제목 (장문에 적용)
        'destination' : f'{phone_num}|{name}', # %고객명% 치환용 입력
        #'rdate' : '예약날짜',
        #'rtime' : '예약시간',
        #'testmode_yn' : '' #테스트모드 적용 여부 Y/N
    }
    send_response = requests.post(send_url, data=sms_data)

    print(send_response.json())    
    return



def send_reservation_confirmed_message(phone_num, name, concert_name, concert_date):
    load_dotenv(os.path.join(os.path.dirname(__file__), '../', 'env'))

    api_key = os.getenv('MESSAGE_API_KEY')
    id_key = os.getenv('MESSAGE_ID')

    send_url = 'https://apis.aligo.in/send/' # 요청을 던지는 URL, 현재는 문자보내기
    sms_data={'key': api_key, #api key
        'userid': id_key, # 알리고 사이트 아이디
        'sender': '01085146141', # 발신번호
        'receiver': phone_num, # 수신번호 (,활용하여 1000명까지 추가 가능)
        'msg': f'%고객명%님 {concert_name}({concert_date}) 버스 대절 예약이 완료되었습니다.\n\nHandybus를 이용해주셔서 감사합니다.', #문자 내용 
        'msg_type' : 'LMS', #메세지 타입 (SMS, LMS)
        'title' : 'Handybus 대절 예약 완료 안내', #메세지 제목 (장문에 적용)
        'destination' : f'{phone_num}|{name}', # %고객명% 치환용 입력
        #'rdate' : '예약날짜',
        #'rtime' : '예약시간',
        #'testmode_yn' : '' #테스트모드 적용 여부 Y/N
    }
    send_response = requests.post(send_url, data=sms_data)

    print(send_response.json())    
    return


@require_POST
def confirmReservationPayment(request, reservation_id):
    payment_type = request.POST.get('payment_type')
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    
    if payment_type == 'pre_reserve':
        reservation.has_paid_pre_reserve_price = True
        send_pre_reservation_confirmed_message(phone_num=reservation.user.phone_number.replace("-",""), name=reservation.user.name, concert_name=reservation.concert.name, concert_date=reservation.concert.date.strftime('%Y-%m-%d'))
        messages.success(request, '선예약금 지불이 확인되었습니다.')
    elif payment_type == 'final_reserve':
        reservation.has_paid_reserve_price = True
        # TODO: undo comment
        # send_reservation_confirmed_message(phone_num=reservation.user.phone_number.replace("-",""), name=reservation.user.name, concert_name=reservation.concert.name, concert_date=reservation.concert.date.strftime('%Y-%m-%d'))
        messages.success(request, '잔금 지불이 확인되었습니다.')
    else:
        messages.error(request, '지불 유형이 올바르지 않습니다.')

    reservation.save()
    
    # Redirect to the reservation status page for this concert
    return redirect('admin:reservationstatus', name=reservation.concert.name)

@login_required
def openChatUrl(request, name):
    # TODO: differenciate before confirmation open chat and after confirmation open chat
    concerts = Concert.objects.filter(name=name).order_by('date')
    open_chat_urls_dict = {}

    for concert in concerts:
        urls = ConcertRegionInfo.objects.filter(concert=concert).order_by('region')
        open_chat_urls_dict[concert] = urls

    if request.method == 'POST':
        region = request.POST.get('region')
        open_chat_url = request.POST.get('open_chat_url')
        concert_id = request.POST.get('concert_id')

        concert = Concert.objects.get(id=concert_id)
        new_url = ConcertRegionInfo.objects.create(concert=concert, region=region, open_chat_url=open_chat_url)

        return redirect('admin:openChatUrl', name=name)

    context = {
        'concerts': concerts,
        'open_chat_urls_dict': open_chat_urls_dict,
        'name': name,
        'regions': Region.choices,
    }

    return render(request, 'handybusmvp/admin/openchaturl.html', context)

@login_required
@require_POST
def updateConcertRegionStatus(request, concert_region_id):
    new_status = request.POST.get('status')
    concert_region_info = get_object_or_404(ConcertRegionInfo, id=concert_region_id)
    concert_region_info.status = new_status
    concert_region_info.save()

    return redirect('admin:openChatUrl', name=concert_region_info.concert.name)


@login_required
def deleteReservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    concert_name = reservation.concert.name
    reservation.delete()
    return redirect('admin:reservationstatus', name=concert_name)


@login_required
def leftseat(request, name):
    # 지역별 그룹화 정보를 가져옵니다.
    grouped_regions = getStopOver(name)
    # print("그룹화된 지역 정보:", grouped_regions)  # 디버깅
    
    # 해당 이름을 가진 콘서트들을 날짜 순으로 가져옵니다.
    concerts = Concert.objects.filter(name=name).order_by('date')
    # print("콘서트 목록:", [str(concert) for concert in concerts])  # 디버깅

    if request.method == 'POST':
        region_seats_input = {}
        for key, value in request.POST.items():
            if key.startswith('region_seats_'):
                concert_id_str, group_name = key.split('_')[-2], key.split('_')[-1]
                region_seats_input[(concert_id_str, group_name)] = int(value)

        # print("POST에서 받은 지역별 좌석 정보:", region_seats_input)  # 디버깅
        
        # 예약 상세 정보를 저장할 빈 딕셔너리 초기화
        reservation_details = {}

        # 입력된 region_seats_input을 순회하면서 처리
        for (concert_id_str, group_name), allocated_seats in region_seats_input.items():
            concert_id = int(concert_id_str)
            concert = get_object_or_404(Concert, id=concert_id)

            if concert not in reservation_details:
                reservation_details[concert] = {}

            upbound_reserved = downbound_reserved = 0
            for region_info in grouped_regions.get(f"{concert.name} / {concert.date.strftime('%Y-%m-%d')}", {}).get(group_name, []):
                upbound_reservations = Reservation.objects.filter(
                    concert=concert,
                    gathering_place_up__region=region_info.region
                ).aggregate(total_upbound=Sum('head_count'))['total_upbound'] or 0

                downbound_reservations = Reservation.objects.filter(
                    concert=concert,
                    gathering_place_down__region=region_info.region
                ).aggregate(total_downbound=Sum('head_count'))['total_downbound'] or 0

                upbound_reserved += upbound_reservations
                downbound_reserved += downbound_reservations

            # 할당된 좌석에서 예약된 좌석 수를 빼서 남은 좌석 수 계산
            upbound_leftseat = allocated_seats - upbound_reserved
            downbound_leftseat = allocated_seats - downbound_reserved

            # 상향 및 하향 남은 좌석 수를 해당 콘서트 및 그룹명에 대한 정보로 저장
            reservation_details[concert][group_name] = {
                'upbound_leftseat': upbound_leftseat,
                'downbound_leftseat': downbound_leftseat
            }

        # print("예약 상세 정보:", reservation_details)

        return render(request, 'handybusmvp/admin/leftseat.html', {
            'grouped_regions': grouped_regions,
            'reservation_details': reservation_details,
            'name': name,
            'concerts': concerts,
        })

    # # POST 요청이 아닐 경우의 처리
    # print("GET 요청 처리")  # 디버깅

    print(getRidingInfoAndReservationStatus(name))
    return render(request, 'handybusmvp/admin/leftseat.html', {'grouped_regions': grouped_regions, 'name': name})


@login_required
def confirmRefund(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.has_refunded = True
    reservation.save()
    return redirect('admin:reservationstatus', name=reservation.concert.name)

# TODO: 내가 알 수 없는 방식으로 작동 중,,, 이해할 필요 있음
@login_required
def confirmOpenChat(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.is_in_open_chat = True
    reservation.save()
    return redirect('admin:reservationstatus', name=reservation.concert.name)

@login_required
def sendOpenChatInvitation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    open_chat_url = ConcertRegionInfo.objects.filter(concert=reservation.concert).last().open_chat_url
    # Gathering place up과 down이 모두 있으면 travel type 왕복
    if reservation.gathering_place_up and reservation.gathering_place_down:
        travel_type = "왕복"
    # Gathering place up만 있으면 travel type 상행
    elif reservation.gathering_place_up:
        travel_type = "상행"
    # Gathering place down만 있으면 travel type 하행
    elif reservation.gathering_place_down:
        travel_type = "하행"

    send_open_chat_invitation_message(phone_num=reservation.user.phone_number.replace("-",""), name=reservation.user.name, concert_name=reservation.concert.name, concert_date=reservation.concert.date, open_chat_url=open_chat_url, trip_type=travel_type)
    return redirect('admin:reservationstatus', name=reservation.concert.name)


def send_open_chat_invitation_message(phone_num, name, concert_name, concert_date, open_chat_url, trip_type):
    modified_name = change_name(name)
    load_dotenv(os.path.join(os.path.dirname(__file__), '../', 'env'))

    api_key = os.getenv('MESSAGE_API_KEY')
    id_key = os.getenv('MESSAGE_ID')

    send_url = 'https://apis.aligo.in/send/' # 요청을 던지는 URL, 현재는 문자보내기
    sms_data={'key': api_key, #api key
        'userid': id_key, # 알리고 사이트 아이디
        'sender': '01085146141', # 발신번호
        'receiver': phone_num, # 수신번호 (,활용하여 1000명까지 추가 가능)
        'msg': f'%고객명%님 {concert_name}({concert_date}) 버스 대절 관련 오픈채팅방으로 입장하지 않으셔서 안내 문자 보내드립니다.\n\n아래 오픈채팅방으로 입장해주세요.\n오픈채팅방 링크: {open_chat_url}\n들어오실 때 이름은 \'{modified_name} / {trip_type} / {phone_num[-4:]}\' 으로 해주세요.\n\nHandybus를 이용해주셔서 감사합니다.', #문자 내용 
        'msg_type' : 'LMS', #메세지 타입 (SMS, LMS)
        'title' : 'Handybus 대절 오픈채팅 입장 안내', #메세지 제목 (장문에 적용)
        'destination' : f'{phone_num}|{name}', # %고객명% 치환용 입력
        #'rdate' : '예약날짜',
        #'rtime' : '예약시간',
        #'testmode_yn' : '' #테스트모드 적용 여부 Y/N
    }
    send_response = requests.post(send_url, data=sms_data)
    return


def requestlist(request):
    # Fetch all ReserveRequest objects from the database
    requests = ReserveRequest.objects.all().order_by('-created_at')
    # Pass the requests to the template
    return render(request, 'handybusmvp/admin/requestlist.html', {'requests': requests})