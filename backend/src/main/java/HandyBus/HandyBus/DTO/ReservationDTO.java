package HandyBus.HandyBus.DTO;

import HandyBus.HandyBus.Domain.ReservationDomain;
import HandyBus.HandyBus.Domain.Subclass.ProceedStatus;
import HandyBus.HandyBus.Domain.Subclass.Region;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.List;
import java.util.stream.Collectors;

@Getter
@Builder
public class ReservationDTO {

    private Long reservationId;
    private ConcertDTO concertDTO;
    private LocalDateTime requiredArriveTime;
    private ProceedStatus proceedStatus;
    private Region region;
    private int price;
    private String qrImage;
    private String chatRoomUrl;
    private String imageUrl;
    private List<UserReservationDTO> userReservationList;

    public static ReservationDTO toDTO(ReservationDomain reservation) {
        return ReservationDTO.builder()
                .reservationId(reservation.getReservationId())
                .requiredArriveTime(reservation.getRequiredArriveTime())
                .proceedStatus(reservation.getProceedStatus())
                .region(reservation.getRegion())
                .price(reservation.getPrice())
                .qrImage(reservation.getQrImage())
                .chatRoomUrl(reservation.getChatRoomUrl())
                .imageUrl(reservation.getImageUrl())
                .userReservationList(reservation.getUserReservationList().stream().map(UserReservationDTO::toDTO).collect(Collectors.toList()))
                .build();
    }

    public ReservationDomain toEntity(){
        return ReservationDomain.builder()
                .concert(this.concertDTO.toEntity())
                .region(this.region)
                .requiredArriveTime(this.requiredArriveTime)
                .proceedStatus(this.proceedStatus)
                .price(this.price)
                .qrImage(this.qrImage)
                .chatRoomUrl(this.chatRoomUrl)
                .imageUrl(this.imageUrl)
                .userReservationList(this.userReservationList.stream().map(UserReservationDTO::toEntity).collect(Collectors.toList()))
                .build();
    }

    @Builder
    public static class SignUp {
        private ConcertDTO concertDTO;
        private String name;
        private Region region;
        private LocalTime requiredArriveTime;
        private String reservationImage;
        private String qrImage;
        private String chatRoomUrl;

        public ReservationDomain toEntity() {
            return ReservationDomain.builder()
                    .concert(this.concertDTO.toEntity())
                    .requiredArriveTime(LocalDateTime.from(this.requiredArriveTime))
                    .qrImage(this.qrImage)
                    .region(this.region)
                    .chatRoomUrl(this.chatRoomUrl)
                    .imageUrl(this.reservationImage)
                    .build();
        }
    }
}
