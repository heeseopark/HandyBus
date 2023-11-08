package HandyBus.HandyBus.Domain;

import HandyBus.HandyBus.Domain.Subclass.Route;
import jakarta.persistence.*;

@Entity
public class BusDomain {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long busID; // Primary key for the bus entity

    @Embedded
    private Route route; // Embedding Route class

    @Column(nullable = false, length = 20)
    private String licensePlate; // License plate string field

    @Column(nullable = false)
    private int capacity; // Bus capacity field

    private int rentalCost; // Rental cost field

    @Column(nullable = false)
    private boolean usable; // Field to indicate if the bus is usable

}