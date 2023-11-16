package HandyBus.HandyBus.NewDTO;

import HandyBus.HandyBus.Domain.ConcertDomain;
import lombok.Getter;
import lombok.Builder;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

@Getter
@Builder
public class ConcertDTO {

    private Long concertId;
    private String name;
    private LocalDate date;
    private LocalTime startTime;
    private LocalTime endTime;
    private String location;
    private String imageUrl;
    private List<ReservationDTO> reservationDTOList;

    public static ConcertDTO toDTO(ConcertDomain concert) {
        return ConcertDTO.builder()
                .concertId(concert.getConcertId())
                .name(concert.getName())
                .date(concert.getDate())
                .startTime(concert.getStartTime())
                .endTime(concert.getEndTime())
                .location(concert.getLocationAddress())
                .imageUrl(concert.getImageUrl())
                .build();
    }

    public ConcertDomain toEntity() {
        return ConcertDomain.builder()
                .name(this.name)
                .date(this.date)
                .startTime(this.startTime)
                .endTime(this.endTime)
                .locationAddress(this.location)
                .imageUrl(this.imageUrl)
                .build();
    }

    @Getter
    @Builder
    public static class SignUp {
        private String name;
        private LocalDate date;
        private LocalTime startTime;
        private LocalTime endTime;
        private String location;
        private String imageUrl;

        public ConcertDomain toEntity() {
            return ConcertDomain.builder()
                    .name(this.name)
                    .date(this.date)
                    .startTime(this.startTime)
                    .endTime(this.endTime)
                    .locationAddress(this.location)
                    .imageUrl(this.imageUrl)
                    .build();
        }
    }
}
