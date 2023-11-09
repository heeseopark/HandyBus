package HandyBus.HandyBus.Domain;

import jakarta.persistence.*;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDate;
import java.time.LocalTime;

@Entity
@Getter
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
    private String locationAddress;

    @Builder
    public ConcertDomain(String name, LocalDate date, LocalTime startTime, LocalTime endTime, String locationAddress){
        this.name = name;
        this.date = date;
        this.startTime = startTime;
        this.endTime = endTime;
        this.locationAddress = locationAddress;
    }
}
