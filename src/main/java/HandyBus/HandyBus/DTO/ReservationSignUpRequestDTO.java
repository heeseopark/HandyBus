package HandyBus.HandyBus.DTO;

import HandyBus.HandyBus.Domain.Subclass.Region;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalTime;

@Getter
@Builder
@AllArgsConstructor
public class ReservationSignUpRequestDTO {


    private ConcertDTO concertDTO;

    private String name;

    private Region region;

    private LocalTime requiredArriveTime;

    private String reservationImage;

    private String qrImage;

    private String chatRoomUrl;


}
