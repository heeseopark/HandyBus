from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import *
import json
from django.db.models import Count
import requests
from dotenv import load_dotenv
from django.contrib import messages
from django.db.models import Min
from .functions import change_name, getRidingInfoAndReservationStatus

# Create your views here.

def index(request):
    # # 선예약 상태인 콘서트만 필터링
    # concert_groups = Concert.objects.filter(status=Concert.Status.PRE_RESERVATION).values('name').annotate(date_count=Count('date')).order_by('name')

    # prereservation_concert_data = []
    # for group in concert_groups:
    #     concerts = Concert.objects.filter(name=group['name'], status=Concert.Status.PRE_RESERVATION).order_by('date')

    #     prereservation_concert_data.append({
    #         'name': group['name'],
    #         'concerts': list(concerts)
    #     })

    # # 실예약 상태인 콘서트만 필터링
    # reservation_concert_groups = Concert.objects.filter(status=Concert.Status.RESERVATION).values('name').annotate(date_count=Count('date')).order_by('name')

    # reservation_concert_data = []
    # for group in reservation_concert_groups:
    #     concerts = Concert.objects.filter(name=group['name'], status=Concert.Status.RESERVATION).order_by('date')

    #     reservation_concert_data.append({
    #         'name': group['name'],
    #         'concerts': list(concerts)
    #     })
    # context = {'prereservation_concert_data': prereservation_concert_data,
    #             'reservation_concert_data': reservation_concert_data}
    # return render(request, 'handybusmvp/user/index.html', context)
    return redirect('user:concertreservationlist')

# 콘서트 현황에 따라서 선입금만 받는 단계이거나 예약까지 받는 단계이거나. 이름고 ㅏ전화번호를 입력하면 예약했던 내역 확인할 수 있게 만들기 그러려면 뷰 함수에 reservation argument도 넣어야 할거 같음.

def concertreservation(request, name):

    if request.method == 'POST':
        # 폼 데이터 처리
        user_name = request.POST.get('user_name')
        phone_number = '-'.join([
            request.POST.get('phone_number_1'),
            request.POST.get('phone_number_2'),
            request.POST.get('phone_number_3')
        ])
        concert_date = request.POST.get('date')
        head_count = int(request.POST.get('head_count'))
        trip_type = request.POST.get('trip_type')
        refund_account = request.POST.get('refund_account_number')

        funnel = request.POST.get('funnel')
        other_inflow = request.POST.get('other_inflow', '').strip()

        if funnel == "기타" and other_inflow:
            final_funnel_value = other_inflow  # 사용자가 입력한 '기타'의 상세 정보를 사용
        else:
            final_funnel_value = funnel  # 기본 유입 경로 사용

        sub_leader_recruitment = request.POST.get('sub_leader_recruitment') == 'yes'

        # Get the IDs for the selected gathering places from the POST data
        gathering_place_up = request.POST.get('upward_regions_places')
        gathering_place_down = request.POST.get('downward_regions_places')
        twitter_image = request.FILES.get('twitter_image')
        instagram_image = request.FILES.get('instagram_image')        

        # 유저 정보 생성 또는 업데이트
        user, created = User.objects.update_or_create(
            phone_number=phone_number,
            defaults={'name': user_name},
        )

        # 선택된 콘서트 정보 가져오기
        concert = Concert.objects.filter(name=name, date=concert_date).first()
        if not concert:
            return render(request, 'handybusmvp/user/error.html', {'message': '콘서트 정보를 찾을 수 없습니다.'})

        if gathering_place_up:
            parts = gathering_place_up.split(' - ')
            if len(parts) == 3:
                region, gathering_place_name, gathering_time_str = parts
                if gathering_time_str == '시간 미정':
                    gathering_time = None
                else:
                    gathering_time = datetime.strptime(gathering_time_str, "%H:%M").time()

                if gathering_time:
                    gathering_place_up_object = GatheringPlace.objects.filter(
                        concert=concert,
                        region=region,
                        name=gathering_place_name,
                        time=gathering_time,
                        direction='upward'
                    ).first()  # 첫 번째 객체를 선택
                else:
                    gathering_place_up_object = GatheringPlace.objects.filter(
                        concert=concert,
                        region=region,
                        name=gathering_place_name,
                        direction='upward'
                    ).first()
        else:
            gathering_place_up_object = None

        if gathering_place_down:
            parts = gathering_place_down.split(' - ')
            if len(parts) == 3:
                region, gathering_place_name, gathering_time_str = parts
                if gathering_time_str == '시간 미정':
                    gathering_time = None
                else:
                    gathering_time = datetime.strptime(gathering_time_str, "%H:%M").time()

                if gathering_time:
                    gathering_place_down_object = GatheringPlace.objects.filter(
                        concert=concert,
                        region=region,
                        name=gathering_place_name,
                        time=gathering_time,
                        direction='downward'
                    ).first()  # 첫 번째 객체를 선택
                else:
                    gathering_place_down_object = GatheringPlace.objects.filter(
                        concert=concert,
                        region=region,
                        name=gathering_place_name,
                        direction='downward'
                    ).first()
        else:
            gathering_place_down_object = None
    
        # 개인정보 동의 버전
        privacy_consent = PrivacyConsent.objects.latest('created_at')

        if not privacy_consent:
            return render(request, 'handybusmvp/user/error.html', {'message': '개인정보 동의 버전을 찾을 수 없습니다.'})
        
        # 예약 객체 생성 전, 선택된 지역의 ConcertRegionInfo 상태에 따라 예약 상태 결정
        region_for_status = gathering_place_up_object.region if gathering_place_up_object else gathering_place_down_object.region
        concert_region_info = ConcertRegionInfo.objects.filter(concert=concert, region=region_for_status).last()

        # ConcertRegionInfo 상태에 따른 Reservation 상태 매핑
        status_mapping = {
            ConcertRegionInfo.StatusChoices.BEFORE_CONFIRMATION: ReservationStatus.BEFORE_FIXED,
            ConcertRegionInfo.StatusChoices.AFTER_CONFIRMATION: ReservationStatus.AFTER_FIXED,
            ConcertRegionInfo.StatusChoices.CLOSED: ReservationStatus.CLOSED,
            ConcertRegionInfo.StatusChoices.CANCELLED: ReservationStatus.CANCELLED,
        }

        # 선택된 지역의 ConcertRegionInfo 상태를 기반으로 예약 상태 설정
        if concert_region_info:
            reservation_status = status_mapping.get(concert_region_info.status, ReservationStatus.BEFORE_FIXED)
        else:
            # ConcertRegionInfo가 없는 경우 기본 상태 설정 (이 경우는 사전에 처리할 수 있는 예외 처리가 필요할 수 있습니다)
            reservation_status = ReservationStatus.BEFORE_FIXED

        # Reservation 객체 생성
        reservation = Reservation.objects.create(
            concert=concert,
            user=user,
            privacy_consent_version=privacy_consent,
            gathering_place_up=gathering_place_up_object,
            gathering_place_down=gathering_place_down_object,
            head_count=head_count,
            has_paid_pre_reserve_price=False,
            has_paid_reserve_price=False,
            funnel=final_funnel_value,
            is_in_charge=sub_leader_recruitment,
            refund_account=refund_account,
            status=reservation_status,
            has_refunded=False,
            is_in_open_chat=False,

        )

        # 동승인 정보 처리
        for i in range(1, head_count):
            companion_name = request.POST.get(f'companion_{i}_name')
            companion_phone = '-'.join([
                request.POST.get(f'companion_{i}_phone_1'),
                request.POST.get(f'companion_{i}_phone_2'),
                request.POST.get(f'companion_{i}_phone_3')
            ])

            Companion.objects.create(
                reservation=reservation,
                name=companion_name,
                phone_number=companion_phone,
            )


        # 이미지 처리 for Twitter
        if twitter_image:
            EventDiscount.objects.create(
                sns_share_image=twitter_image,
                sns_type='twitter',  # Set the sns_type explicitly for Twitter
                reservation=reservation  # Assume you've already created a Reservation instance above
            )

        # 이미지 처리 for Instagram
        if instagram_image:
            EventDiscount.objects.create(
                sns_share_image=instagram_image,
                sns_type='instagram',  # Set the sns_type explicitly for Instagram
                reservation=reservation  # Use the same Reservation instance if applicable
            )

        # TODO: add price calculating logic
            
        pricing_info = Pricing.objects.filter(
            concert=concert, 
            region=reservation.gathering_place_up.region if reservation.gathering_place_up else reservation.gathering_place_down.region
        ).first()

        if pricing_info:
            # pre_reserve_price와 reservation의 head_count를 곱하여 최종 가격을 계산
            price = pricing_info.pre_reserve_price * reservation.head_count
        else:
            # 적절한 가격 정보가 없는 경우, 오류 처리 또는 기본값 설정
            price = 0  # 또는 적절한 기본값 설정
        
        # 상행지 혹은 하행지 지역을 기준으로 오픈채팅방 URL 조회
        region_for_url = reservation.gathering_place_up.region if reservation.gathering_place_up else reservation.gathering_place_down.region

        if reservation.status == ReservationStatus.BEFORE_FIXED:
            open_chat_url = Concert.objects.filter(name=name, date=concert_date).last().concert_open_chat_url
        elif reservation.status == ReservationStatus.AFTER_FIXED:
            open_chat_url = ConcertRegionInfo.objects.filter(concert=concert, region=region_for_url).last()

        if gathering_place_up_object and not gathering_place_down_object:
            trip_type = '상행'
        elif not gathering_place_up_object and gathering_place_down_object:
            trip_type = '하행'
        elif gathering_place_up_object and gathering_place_down_object:
            trip_type = '왕복'
        else:
            trip_type = '미정'
        send_reservation_registered_message(phone_num=phone_number.replace("-",""), name=user_name, concert_name=name, concert_date=concert_date, price=price, open_chat_url=open_chat_url, trip_type=trip_type)
        request.session['reservation_id'] = reservation.id
        request.session['pre_reservation_price'] = str("{:,}".format(price))
        request.session['open_chat_url'] = open_chat_url
        request.session['entrance_name'] = f'{change_name(user_name)} / {trip_type} / {phone_number[-4:]}'  # 입장 시 사용할 이름
        # 리다이렉트
        return redirect('user:reservationdone')  # 적절한 URL 네임으로 대체하세요.

    # name에 해당하는 콘서트를 가져오되, 'reservation' 상태인 콘서트만 필터링
    concerts = Concert.objects.filter(name=name, status=Concert.Status.RESERVATION).order_by('date')
    
    # 'reservation' 상태의 콘서트가 없으면 error.html을 랜더링
    if not concerts:
        return render(request, 'handybusmvp/user/error.html', {'message': '해당 대절은 실예약 가능 상태가 아닙니다.'})
    concert_place = concerts.first().location
    privacyConsent = PrivacyConsent.objects.latest('created_at')

    riding_and_status_info = getRidingInfoAndReservationStatus(name)

    reservationInfo = {}
    for concert in concerts:
        date_str = concert.date.strftime('%Y-%m-%d')
        regionsPlaces = {'upward': {}, 'downward': {}}

        # 콘서트에 대한 대절 확정 정보를 조회
        confirmed_regions = ConcertRegionInfo.objects.filter(
            concert=concert,
            status__in=[ConcertRegionInfo.StatusChoices.BEFORE_CONFIRMATION, ConcertRegionInfo.StatusChoices.AFTER_CONFIRMATION]
        ).values_list('region', flat=True)

        for place in GatheringPlace.objects.filter(concert=concert, region__in=confirmed_regions):
            direction = place.direction
            region = place.region

            # 대절 확정 지역만 처리
            if direction in regionsPlaces and region in confirmed_regions:
                if region not in regionsPlaces[direction]:
                    regionsPlaces[direction][region] = []
                time_str = ''
                if place.time:
                    time_str = place.time.strftime('%H:%M')
                else:
                    time_str = '시간 미정'
                regionsPlaces[direction][region].append({
                    'name': place.name,
                    'time': time_str,
                    'location': place.location if place.location else ''
                })

        reservationInfo[date_str] = regionsPlaces
    concert = concerts.first()
    pricings = Pricing.objects.filter(concert=concert).all() # 첫번째 콘서트의 객체를 가지고 올 수 있게

    context = {
        'concertplace': concert_place,
        'concertname': name,
        'pricings': pricings,
        'privacyConsent': privacyConsent,
        'reservationInfo': json.dumps(reservationInfo, ensure_ascii=False),
        'concert_image_url': concert.image.url,
        'riding_and_status_info': riding_and_status_info,
    }

    return render(request, 'handybusmvp/user/concertreservation.html', context)


def prereservation(request, name):
    if request.method == 'POST':
        # 폼 데이터 처리
        user_name = request.POST.get('user_name')
        phone_number = '-'.join([request.POST.get('phone_number_1'), request.POST.get('phone_number_2'), request.POST.get('phone_number_3')])
        concert_date = request.POST.get('concert_date')
        region = request.POST.get('region')
        head_count = int(request.POST.get('head_count'))
        trip_type = request.POST.get('trip_type')
        
        # 여행 타입에 따른 upbound, downbound 설정
        is_upbound = trip_type in ['round_trip', 'one_way_to']
        is_downbound = trip_type in ['round_trip', 'one_way_back']

        # 유저 정보 생성 또는 업데이트
        user, created = User.objects.update_or_create(
            phone_number=phone_number,
            defaults={'name': user_name},
        )



        # 선택된 콘서트 정보 가져오기
        concert = Concert.objects.filter(name=name, date=concert_date).first()

        # 개인정보 동의 버전
        privacy_consent = PrivacyConsent.objects.latest('created_at')
        
        # PreReservation 객체 생성
        pre_reservation = PreReservation.objects.create(
            concert=concert,
            user=user,
            privacy_consent_version=privacy_consent,
            region=region,
            head_count=head_count,
            is_upbound=is_upbound,
            is_downbound=is_downbound,
        )

        # 동승인 정보 처리
        for i in range(1, head_count):
            companion_name = request.POST.get(f'companion_{i}_name')
            companion_phone = '-'.join([
                request.POST.get(f'companion_{i}_phone_1'),
                request.POST.get(f'companion_{i}_phone_2'),
                request.POST.get(f'companion_{i}_phone_3')
            ])

            SurveyCompanion.objects.create(
                pre_reservation=pre_reservation,
                name=companion_name,
                phone_number=companion_phone,
            )

        request.session['prereservation_id'] = pre_reservation.id

        send_pre_reservation_done_message(phone_num=phone_number.replace("-",""), name=user_name, concert_name=concert.name, concert_date=concert_date)
        return redirect('user:prereservationdone')

    concerts = Concert.objects.filter(name=name, status=Concert.Status.PRE_RESERVATION).order_by('date')
    if not concerts:
        return render(request, 'handybusmvp/user/error.html', {'message': '해당 대절은 현재 수요조사를 받고 있지 않습니다.'})
    
    concert_image_url = concerts.first().image.url if concerts.first().image else None

    privacyConsent = PrivacyConsent.objects.latest('created_at')
    dates = concerts.values_list('date', flat=True).distinct()
    dates = [date.strftime('%Y-%m-%d') for date in dates]
    regions = [{'code': region[0], 'name': region[1]} for region in Region.choices]

    context = {
        'concertname': name,
        'privacyConsent': privacyConsent,
        'dates': dates,
        'regions': regions,
        'concert_image_url': concert_image_url,
    }

    return render(request, 'handybusmvp/user/prereservation.html', context)

def checkprereservation(request):
    concerts = Concert.objects.filter(status=Concert.Status.PRE_RESERVATION).order_by('name')
    regions = Region.choices

    # 폼을 렌더링하는데 필요한 컨텍스트를 전달합니다.
    return render(request, 'handybusmvp/user/checkprereservation.html', {
        'concerts': concerts,
        'regions': regions,
    })

def checkprereservationinfo(request):
    concerts = Concert.objects.filter(status=Concert.Status.PRE_RESERVATION).order_by('name')
    regions = Region.choices
    pre_reservation_info = None
    companions_info = []
    if request.method == 'POST':
        concert_id = request.POST.get('concert_name')
        region_code = request.POST.get('region')
        name = request.POST.get('name')
        phone_number_parts = [
            request.POST.get('phone_number_1'),
            request.POST.get('phone_number_2'),
            request.POST.get('phone_number_3')
        ]
        phone_number = '-'.join(phone_number_parts)  # 예: '010-1234-5678'
        # 사용자의 선예약 정보 조회
        pre_reservation = PreReservation.objects.filter(
            concert_id=concert_id,
            user__name=name,
            user__phone_number=phone_number,
            region=region_code
        ).select_related('concert', 'user').first()

        if pre_reservation:
            pricing = Pricing.objects.filter(
                concert_id=concert_id,
                region=region_code
            ).first()

            total_price = pricing.pre_reserve_price * pre_reservation.head_count if pricing else None

            companions = Companion.objects.filter(pre_reservation=pre_reservation).all()

            for companion in companions:
                companions_info.append({
                    'name': companion.name,
                    'phone_number': companion.phone_number
                })

            pre_reservation_info = {
                'concert_name': pre_reservation.concert.name,
                'concert_date': pre_reservation.concert.date,
                'region': pre_reservation.region,
                'head_count': pre_reservation.head_count,
                'total_price': total_price,
                'has_paid': pre_reservation.has_paid,
                'created_at': pre_reservation.created_at,
                'updated_at': pre_reservation.updated_at,
                'companions': companions_info,  # 동승인 정보 추가
            }

        # 조회된 정보를 템플릿에 전달합니다.
        return render(request, 'handybusmvp/user/checkprereservationinfo.html', {
            'pre_reservation_info': pre_reservation_info,
            'concerts': concerts,
            'regions': regions,
        })
    else:
        # POST 요청이 아닌 경우, 폼 입력 페이지로 리다이렉트합니다.
        return redirect('user:checkprereservation')


def concertprereservationlist(request):
    # 선예약 상태인 콘서트만 필터링
    concert_groups = Concert.objects.filter(status=Concert.Status.PRE_RESERVATION) \
        .values('name') \
        .annotate(first_concert_date=Min('date')) \
    .order_by('first_concert_date')
    concert_data = []
    for group in concert_groups:
        concerts = Concert.objects.filter(name=group['name'], status=Concert.Status.PRE_RESERVATION).order_by('date')

        concert_data.append({
            'name': group['name'],
            'concerts': list(concerts)
        })

    context = {'concert_data': concert_data}
    return render(request, 'handybusmvp/user/prereservationlist.html', context)

def concertreservationlist(request):
    # 실예약 상태인 콘서트만 필터링
    concert_groups = Concert.objects.filter(status=Concert.Status.RESERVATION).values('name').annotate(date_count=Count('date')).order_by('name')

    concert_data = []
    for group in concert_groups:
        concerts = Concert.objects.filter(name=group['name'], status=Concert.Status.RESERVATION).order_by('date')

        concert_data.append({
            'name': group['name'],
            'concerts': list(concerts)
        })

    context = {'concert_data': concert_data}
    return render(request, 'handybusmvp/user/reservationlist.html', context)

def checkreservation(request):
    concerts = Concert.objects.filter(status=Concert.Status.RESERVATION).order_by('date')
    regions = Region.choices

    # 폼을 렌더링하는데 필요한 컨텍스트를 전달합니다.
    return render(request, 'handybusmvp/user/checkreservation.html', {
        'concerts': concerts,
        'regions': regions,
    })

def checkreservationinfo(request):
    concerts = Concert.objects.filter(status=Concert.Status.RESERVATION).order_by('date')
    regions = Region.choices

    if request.method == 'POST':
        concert_id = request.POST.get('concert_name')
        name = request.POST.get('name')
        phone_number_parts = [
            request.POST.get('phone_number_1'),
            request.POST.get('phone_number_2'),
            request.POST.get('phone_number_3')
        ]
        phone_number = '-'.join(phone_number_parts)  # 예: '010-1234-5678'
        
        # 사용자의 실예약 정보 조회
        reservation = Reservation.objects.filter(
            concert_id=concert_id,
            user__name=name,
            user__phone_number=phone_number
        ).last()

        if not reservation:
            return render(request, 'handybusmvp/user/checkreservationinfo.html', {
                'concerts': concerts,
                'regions': regions,
            })

        
        # region_display는 get_region_display()를 사용해서 설정
        if reservation.gathering_place_up:
            reservation.region_display = reservation.gathering_place_up.get_region_display()
        elif reservation.gathering_place_down:
            reservation.region_display = reservation.gathering_place_down.get_region_display()
        else:
            reservation.region_display = "No region"  # or some default value
        
        # trip_type 설정
        if reservation.gathering_place_up and reservation.gathering_place_down:
            reservation.trip_type = '왕복'
        elif reservation.gathering_place_up:
            reservation.trip_type = '상행'
        elif reservation.gathering_place_down:
            reservation.trip_type = '하행'
        else:
            reservation.trip_type = '정보 없음'

        reservation.region = reservation.gathering_place_up.region if reservation.gathering_place_up else reservation.gathering_place_down.region
        # ConcertRegionInfo에서 reserve_status 설정
        concertregioninfo = ConcertRegionInfo.objects.filter(concert=reservation.concert, region=reservation.region).last()
        if concertregioninfo:
            reserve_status_display = concertregioninfo.get_status_display()
            reserve_status = concertregioninfo.status
        else:
            reserve_status_display = '정보 없음'
            reserve_status = None
        reservation.reserve_status = reserve_status
        reservation.reserve_status_display = reserve_status_display

        pricing = Pricing.objects.filter(concert_id=concert_id, region=reservation.region).last()
        if pricing:
            reservation.pre_reserve_price = pricing.pre_reserve_price * reservation.head_count
            # trip_type에 따른 가격 계산
            if reservation.trip_type == '왕복':
                reservation.reserve_price = pricing.round_trip_price * reservation.head_count
            elif reservation.trip_type == '상행':
                reservation.reserve_price = pricing.upbound_price * reservation.head_count
            elif reservation.trip_type == '하행':
                reservation.reserve_price = pricing.downbound_price * reservation.head_count
            else:
                reservation.reserve_price = 0  # '정보 없음' 또는 다른 조건에 대한 처리

        # SNS 공유에 따른 할인 적용
        discount_amount = 0
        if EventDiscount.objects.filter(reservation=reservation, sns_type=SNS.TWITTER).exists():
            discount_amount += 1000  # 트위터 공유 할인
        if EventDiscount.objects.filter(reservation=reservation, sns_type=SNS.INSTAGRAM).exists():
            discount_amount += 1000  # 인스타그램 공유 할인

        # 할인된 금액을 최종 예약 가격에서 차감
        reservation.reserve_price -= discount_amount
                
        # reservation의 상태가 BEFORE_CONFIRMATION인 경우, 사전 예약 금액 차감
        if reservation.status == ReservationStatus.BEFORE_FIXED:
            reservation.reserve_price -= reservation.pre_reserve_price

        # 조회된 정보를 템플릿에 전달합니다.
        return render(request, 'handybusmvp/user/checkreservationinfo.html', {
            'reservation': reservation,
            'concerts': concerts,
            'regions': regions,
        })
    else:
        # POST 요청이 아닌 경우, 폼 입력 페이지로 리다이렉트합니다.
        return redirect('user:checkreservation')

    

def send_pre_reservation_done_message(phone_num, name, concert_name, concert_date):
    load_dotenv(os.path.join(os.path.dirname(__file__), '../', 'env'))

    api_key = os.getenv('MESSAGE_API_KEY')
    id_key = os.getenv('MESSAGE_ID')

    send_url = 'https://apis.aligo.in/send/' # 요청을 던지는 URL, 현재는 문자보내기
    sms_data={'key': api_key, #api key
        'userid': id_key, # 알리고 사이트 아이디
        'sender': '01085146141', # 발신번호
        'receiver': phone_num, # 수신번호 (,활용하여 1000명까지 추가 가능)
        'msg': f'%고객명%님 {concert_name}({concert_date}) 버스 대절 수요조사가 접수되었습니다.\n\n대절 모집으로 진행되는 경우 추가 문자로 다시 안내해드리겠습니다.\n\nHandybus를 이용해주셔서 감사합니다:)', #문자 내용 
        'msg_type' : 'LMS', #메세지 타입 (SMS, LMS)
        'title' : 'Handybus 수요조사 안내', #메세지 제목 (장문에 적용)
        'destination' : f'{phone_num}|{name}', # %고객명% 치환용 입력
        #'rdate' : '예약날짜',
        #'rtime' : '예약시간',
        #'testmode_yn' : '' #테스트모드 적용 여부 Y/N
    }
    send_response = requests.post(send_url, data=sms_data)

    print(send_response.json())    
    return
    

def send_reservation_registered_message(phone_num, name, concert_name, concert_date, price, open_chat_url, trip_type):
    modified_name = change_name(name)
    load_dotenv(os.path.join(os.path.dirname(__file__), '../', 'env'))

    api_key = os.getenv('MESSAGE_API_KEY')
    id_key = os.getenv('MESSAGE_ID')

    send_url = 'https://apis.aligo.in/send/' # 요청을 던지는 URL, 현재는 문자보내기
    sms_data={'key': api_key, #api key
        'userid': id_key, # 알리고 사이트 아이디
        'sender': '01085146141', # 발신번호
        'receiver': phone_num, # 수신번호 (,활용하여 1000명까지 추가 가능)
        'msg': f'%고객명%님 {concert_name}({concert_date}) 버스 대절 예약이 접수되었습니다. 아래의 내용을 따라주시면 감사하겠습니다.\n\n\n1. 가신청 금액 {"{:,}".format(price)}원을 아래 계좌로 보내주시기 바랍니다.\n입금 계좌: 카카오뱅크 7979-78-00425 ㅈㅈㅇ\n\n\n2. 아래 오픈채팅방으로 입장해주세요.\n오픈채팅방 링크: {open_chat_url}\n들어오실 때 이름은 \'{modified_name} / {trip_type} / {phone_num[-4:]}\' 으로 해주세요.\n\n대절 확정/무산 결정 시 추가 문자로 안내드리겠습니다.\n\nHandybus를 이용해주셔서 감사합니다.', #문자 내용 
        'msg_type' : 'LMS', #메세지 타입 (SMS, LMS)
        'title' : 'Handybus 대절 예약 접수 안내', #메세지 제목 (장문에 적용)
        'destination' : f'{phone_num}|{name}', # %고객명% 치환용 입력
        #'rdate' : '예약날짜',
        #'rtime' : '예약시간',
        #'testmode_yn' : '' #테스트모드 적용 여부 Y/N
    }
    send_response = requests.post(send_url, data=sms_data)
    return
    
def reservationDone(request):
    # 세션에서 예약 ID 가져오기
    reservation_id = request.session.get('reservation_id')
    pre_reserve_price = request.session.get('pre_reservation_price')
    open_chat_url = request.session.get('open_chat_url')
    entrance_name = request.session.get('entrance_name')
    # TODO: reservation 객체 자체를 세션에 담아서 가지고 올 수 있는지 확인하기.

        # 아래의 관리자 페이지 로직을 참고해서 가격 정보 책정하기
        # reservations = Reservation.objects.filter(concert=concert)\
        #     .select_related('user', 'gathering_place_up', 'gathering_place_down')\
        #     .prefetch_related('reservation_companions', 'eventdiscount_set')\
        #     .annotate(
        #         up_region=F('gathering_place_up__region'),
        #         down_region=F('gathering_place_down__region'),
        #         up_exists=Exists(GatheringPlace.objects.filter(id=OuterRef('gathering_place_up_id'))),
        #         down_exists=Exists(GatheringPlace.objects.filter(id=OuterRef('gathering_place_down_id'))),
        #         twitter_discount_exists=Exists(EventDiscount.objects.filter(reservation=OuterRef('pk'), sns_type=SNS.TWITTER)),
        #         instagram_discount_exists=Exists(EventDiscount.objects.filter(reservation=OuterRef('pk'), sns_type=SNS.INSTAGRAM)),
        #     ).annotate(
        #         pre_reserve_deposit=Case(
        #             When(up_exists=True, then=Subquery(
        #                 Pricing.objects.filter(
        #                     concert=concert,
        #                     region=OuterRef('up_region')
        #                 ).values('pre_reserve_price')[:1]
        #             ) * F('head_count')),
        #             When(down_exists=True, then=Subquery(
        #                 Pricing.objects.filter(
        #                     concert=concert,
        #                     region=OuterRef('down_region')
        #                 ).values('pre_reserve_price')[:1]
        #             ) * F('head_count')),
        #             default=Value(0),
        #             output_field=DecimalField()
        #         ),
        #         trip_price=Case(
        #             When(up_exists=True, down_exists=True, then=Subquery(
        #                 Pricing.objects.filter(
        #                     concert=concert,
        #                     region=OuterRef('up_region')
        #                 ).values('round_trip_price')[:1]
        #             )),
        #             When(up_exists=True, down_exists=False, then=Subquery(
        #                 Pricing.objects.filter(
        #                     concert=concert,
        #                     region=OuterRef('up_region')
        #                 ).values('upbound_price')[:1]
        #             )),
        #             When(up_exists=False, down_exists=True, then=Subquery(
        #                 Pricing.objects.filter(
        #                     concert=concert,
        #                     region=OuterRef('down_region')
        #                 ).values('downbound_price')[:1]
        #             )),
        #             default=Value(0),
        #             output_field=DecimalField()
        #         ) * F('head_count')
        #     ).annotate(
        #         discount_amount=Case(
        #             When(twitter_discount_exists=True, instagram_discount_exists=True, then=Value(2000)),
        #             When(twitter_discount_exists=True, then=Value(1000)),
        #             When(instagram_discount_exists=True, then=Value(1000)),
        #             default=Value(0),
        #             output_field=DecimalField()
        #         )
        #     ).annotate(
        #         required_deposit=Case(
        #             When(status=ReservationStatus.BEFORE_FIXED, then=F('trip_price') - F('discount_amount') - F('pre_reserve_deposit')),
        #             When(status=ReservationStatus.AFTER_FIXED, then=F('trip_price') - F('discount_amount')),
        #             default=F('trip_price') - F('discount_amount'), # Other status cases
        #             output_field=DecimalField()
        #         )
        #     ).order_by('created_at')

    # reservation.reserve_price = 이 내용 채우기

    if reservation_id:
        reservation = get_object_or_404(Reservation, id=reservation_id)
        # TODO: 대절 확정 이후 예약 다루기
        reservation = get_object_or_404(Reservation, id=reservation_id)
        concert = reservation.concert
        
        # 가격 정보 책정 로직
        pricing_info = Pricing.objects.filter(
            concert=concert,
            region=reservation.gathering_place_up.region if reservation.gathering_place_up else reservation.gathering_place_down.region if reservation.gathering_place_down else None
        ).last()
        
        if pricing_info:
            base_price = pricing_info.pre_reserve_price * reservation.head_count
        else:
            base_price = 0
        
        discount_amount = 0
        if EventDiscount.objects.filter(reservation=reservation, sns_type=SNS.TWITTER).exists():
            discount_amount += 1000
        if EventDiscount.objects.filter(reservation=reservation, sns_type=SNS.INSTAGRAM).exists():
            discount_amount += 1000
        
        # 최종 가격 책정
        final_price = max(base_price - discount_amount, 0)
        
        reservation.reserve_price = final_price

        # 필요한 정보를 컨텍스트에 담음
        context = {
            'name': reservation.user.name,
            'phone_num': reservation.user.phone_number,
            'concert_name': reservation.concert.name,
            'concert_date': reservation.concert.date,
            'concert_image_url': reservation.concert.image.url,
            'pre_reserve_price': pre_reserve_price,
            'open_chat_url': open_chat_url,
            'entrance_name': entrance_name,
            'reservation_status': reservation.status,
            'reserve_price': reservation.reserve_price,
            # 여기에 필요한 다른 정보 추가
        }

        # 세션에서 예약 ID 삭제 (선택적)
        del request.session['reservation_id']
    else:
        context = {
            'message': '유효한 예약 정보를 찾을 수 없습니다.'
        }


    return render(request, 'handybusmvp/user/reservationdone.html', context)

def prereservationdone(request):
    # 세션에서 예약 ID 가져오기
    prereservation_id = request.session.get('prereservation_id')

    if prereservation_id:
        reservation = get_object_or_404(PreReservation, id=prereservation_id)

        # 필요한 정보를 컨텍스트에 담음
        context = {
            'name': reservation.user.name,
            'phone_num': reservation.user.phone_number,
            'concert_name': reservation.concert.name,
            'concert_date': reservation.concert.date,
            'concert_image_url': reservation.concert.image.url,


            # 여기에 필요한 다른 정보 추가
        }

        # 세션에서 예약 ID 삭제 (선택적)
        del request.session['prereservation_id']
    else:
        context = {
            'message': '유효한 수요조사 접수 정보를 찾을 수 없습니다.'
        }


    return render(request, 'handybusmvp/user/prereservationdone.html', context)

def reserverequest(request):
    if request.method == 'POST':
        # Extract data from the form
        name = request.POST.get('user_name')
        # Concatenate phone number parts
        phone_number = '-'.join([
            request.POST.get('phone_number_1', ''),
            request.POST.get('phone_number_2', ''),
            request.POST.get('phone_number_3', '')
        ])
        region = request.POST.get('region')
        other_region = request.POST.get('other_region', '').strip()
        request_content = request.POST.get('reservation_request')
        
        # If '기타' region is selected and other_region is provided, use other_region as the region
        if region == '기타' and other_region:
            region = other_region

        # Create and save the ReserveRequest object
        reserve_request = ReserveRequest(
            name=name,
            phone_number=phone_number,
            region=region,
            request_content=request_content
        )
        reserve_request.save()

        # Redirect to a new URL after POST
        return redirect('user:requestdone')
    
    # If not POST, render the form again
    return render(request, 'handybusmvp/user/reserverequest.html')


def requestdone(request):
    return render(request, 'handybusmvp/user/requestdone.html')