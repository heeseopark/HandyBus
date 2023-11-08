package HandyBus.HandyBus.DTO;


import HandyBus.HandyBus.Domain.Subclass.Address;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.time.LocalTime;

@Getter
@NoArgsConstructor
public class ConcertSignUpDTO {

    private String name;
    private LocalDate date;
    private LocalTime startTime;
    private LocalTime endTime;
    private Address location;
}
