package HandyBus.HandyBus.Domain;

import HandyBus.HandyBus.Domain.Subclass.Address;
import jakarta.persistence.*;
import java.time.LocalDate;
import java.time.LocalTime;

@Entity
public class ConcertDomain {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id; // Primary key for the concert entity

    @JoinColumn(name = "idol_id")
    private Long idolID; // Assuming there's an IdolDomain entity for the idol

    @Column(nullable = false, length = 100)
    private String name; // Concert name

    @Column(nullable = false)
    private LocalDate date; // Date of the concert

    @Column(nullable = false)
    private LocalTime startTime; // Start time of the concert

    @Column(nullable = false)
    private LocalTime endTime; // End time of the concert

    @Embedded
    @Column(nullable = false)
    private Address location; // Embeddable Address class

    // Getters and setters for all fields

    // Assuming Address is a class marked with @Embeddable annotation


    // Constructor, getters, and setters...
}
