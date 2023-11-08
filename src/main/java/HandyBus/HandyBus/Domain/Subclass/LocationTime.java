package HandyBus.HandyBus.Domain.Subclass;

import HandyBus.HandyBus.Domain.Subclass.Address;
import jakarta.persistence.Embeddable;
import jakarta.persistence.Embedded;

import java.time.LocalTime;

public class LocationTime {


    @Embeddable
    public static class LocationTime {
        @Embedded
        private Address address; // Uses the Address class from ConcertDomain
        private LocalTime time; // Time information

        // Getters and setters for address and time
    }
}
