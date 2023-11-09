package HandyBus.HandyBus.DTO;


import HandyBus.HandyBus.Domain.Subclass.Address;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDate;
import java.time.LocalTime;

@Getter
@Builder
@AllArgsConstructor
public class ConcertDTO {

    private String name;
    private LocalDate date;
    private LocalTime startTime;
    private LocalTime endTime;
    private Address location;
}
