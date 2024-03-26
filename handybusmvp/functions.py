from .models import Concert, ConcertRegionInfo, GatheringPlace, Direction

def change_name(name):
    # 이름의 길이에 따라 다르게 처리
    if len(name) > 2:
        # 이름의 가운데를 '*'로 바꿈. 첫 글자와 마지막 글자 사이에 '*'를 삽입
        # 첫 글자 + '*' + 마지막 글자
        return name[0] + '*' * (len(name) - 2) + name[-1]
    elif len(name) == 2:
        # 이름이 두 글자인 경우, 뒤에 '*' 추가
        return name[0] + '*'
    else:
        # 이름이 한 글자인 경우, 그대로 반환 (이 경우는 문제에서 언급되지 않았으므로 추가적인 처리가 필요 없음)
        return name
    
def getStopOver(name):
    concerts = Concert.objects.filter(name=name).order_by('date')
    concerts_grouped_regions = {}  # This dictionary will store each concert's grouped regions

    for concert in concerts:
        region_infos = ConcertRegionInfo.objects.filter(concert=concert).order_by('region')
        grouped_regions = {}  # Dictionary to hold region names as keys and lists of regions as values for the current concert
        group_tracker = {}  # Dictionary to track which group a region is at in grouped_regions for the current concert

        for region_info in region_infos:
            region_name = region_info.get_region_display()  # Get the display name of the region
            group = region_info.stopover_group
            if group is not None:
                if group in group_tracker:
                    # If the group already has an entry, append to that entry and update the key with concatenated region names
                    key = group_tracker[group]
                    grouped_regions[key].append(region_info)
                    # Update the key to include the new region name, ensuring unique concatenated names for each group
                    new_key = f"{key}/{region_name}"
                    grouped_regions[new_key] = grouped_regions.pop(key)
                    group_tracker[group] = new_key
                else:
                    # If the group doesn't have an entry yet, create a new entry in grouped_regions with the region name as the key
                    grouped_regions[region_name] = [region_info]
                    group_tracker[group] = region_name
            else:
                # For standalone regions, use the region name as the key
                if region_name in grouped_regions:
                    # If the region name already exists, append to the list
                    grouped_regions[region_name].append(region_info)
                else:
                    # Otherwise, create a new entry
                    grouped_regions[region_name] = [region_info]

        # Assign the grouped regions for this concert to the main dictionary
        concerts_grouped_regions[f"{concert.name} / {concert.date.strftime('%Y-%m-%d')}"] = grouped_regions

    # Optionally, print the structured data for each concert
    # for concert_key, grouped_regions in concerts_grouped_regions.items():
    #     print(f"Concert: {concert_key}")
    #     for key, value in grouped_regions.items():
    #         print(f" Regions Group: {key}")
    #         for region_info in value:
    #             print(f"  - Region: {region_info.get_region_display()}, Stopover Group: {region_info.stopover_group}")
    print(concerts_grouped_regions)
    return concerts_grouped_regions


def getRidingInfoAndReservationStatus(name):
    stopovers = getStopOver(name)  # 콘서트별 지역 정보 그룹화 가져오기
    riding_and_status_info = {}  # 최종 정보를 담을 딕셔너리

    for concert in stopovers.keys():
        concert_date = concert.split(' / ')[-1][-2:]  # 날짜 정보 추출
        regions = stopovers[concert]
        region_status_dict = {}  # 지역별 예약 상태를 저장할 딕셔너리

        for region_group, region_infos in regions.items():
            time_defined = []  # 시간이 정해진 장소 정보
            time_undefined = []  # 시간 미정 장소 정보

            # 모든 지역 정보를 순회하여 탑승 장소 정보 모으기
            for region_info in region_infos:
                gathering_places = GatheringPlace.objects.filter(
                    concert=region_info.concert,
                    region=region_info.region,
                    direction=Direction.UPWARD,
                ).order_by('time', 'name')
                
                for place in gathering_places:
                    if place.time:
                        time_str = place.time.strftime("%H:%M")
                        time_defined.append({"name": place.name, "time": time_str})
                    else:
                        time_undefined.append({"name": place.name, "time": "시간 미정"})

            # 각 지역별 예약 상태 정보 수집
            status_dict = {region_info.get_region_display(): region_info.get_status_display()
                            for region_info in region_infos}

            # 지역 그룹별 정보 업데이트
            region_status_dict[region_group] = {
                "time_defined": time_defined,
                "time_undefined": time_undefined,
                "reservation_status": status_dict
            }

        # 최종 정보 업데이트
        riding_and_status_info[concert_date] = region_status_dict

    print(riding_and_status_info)
    return riding_and_status_info





# TODO: make function that creates default price and gathering place datas