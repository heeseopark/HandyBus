package HandyBus.HandyBus.NewDTO;

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
                .price(reservation.getPrice())
                .qrImage(reservation.getQrImage())
                .chatRoomUrl(reservation.getChatRoomUrl())
                .imageUrl(reservation.getImageUrl())
                .userReservationList(reservation.getUserReservationList().stream().map(UserReservationDTO::toDTO).collect(Collectors.toList()))
                .build();
    }
    
    @Getter
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
                    .chatRoomUrl(this.chatRoomUrl)
                    .imageUrl(this.reservationImage)
                    .build();
        }
    }
}
