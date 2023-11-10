package HandyBus.HandyBus.Domain;

import jakarta.persistence.*;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

@Entity
@Getter
public class ConcertDomain {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "idol_id")
    private IdolDomain idol;

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

    @OneToMany(mappedBy = "concertID")
    private List<ReservationDomain> reservationList; // One-to-many relationship with ReservationDomain

    private String imageUrl;

    @Builder
    public ConcertDomain(String name, LocalDate date, LocalTime startTime, LocalTime endTime, String locationAddress){
        this.name = name;
        this.date = date;
        this.startTime = startTime;
        this.endTime = endTime;
        this.locationAddress = locationAddress;
    }
}
