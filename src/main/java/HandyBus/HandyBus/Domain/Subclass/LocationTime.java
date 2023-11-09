package HandyBus.HandyBus.Domain.Subclass;

import jakarta.persistence.Embeddable;
import jakarta.persistence.Embedded;
import lombok.Getter;

import java.time.LocalTime;

@Embeddable
@Getter
public class LocationTime {
    @Embedded
    private String postCode;
    private LocalTime time;

}

