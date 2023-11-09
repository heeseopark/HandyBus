package HandyBus.HandyBus.Domain.Subclass;

import jakarta.persistence.Embeddable;
import lombok.AllArgsConstructor;

@Embeddable
@AllArgsConstructor
public class Address {
    private String street;
    private String city;
    private String state;
    private String postalCode;
    private String country;

    // Constructors, getters, and setters
}
