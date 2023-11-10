package HandyBus.HandyBus.DTO;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

public class ConcertAndReservationDTO {

    private String idolName;
    private String concertName;
    private String name;
    private LocalDate date;
    private LocalTime startTime;
    private LocalTime endTime;
    private String location;
    private List<ReservationListDTO> reservationList;
}
