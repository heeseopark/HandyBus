package HandyBus.HandyBus.Domain;

import jakarta.persistence.*;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Getter
public class ConcertDomain {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
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

    @Column(nullable = false)
    private String locationAddress;

    @OneToMany(mappedBy = "concertID", cascade = CascadeType.ALL)
    private List<ReservationDomain> reservationList = new ArrayList<>(); // One-to-many relationship with ReservationDomain

    private String imageUrl;

    @Builder
    public ConcertDomain(String name, LocalDate date, LocalTime startTime, LocalTime endTime, String locationAddress, String imageUrl){
        this.name = name;
        this.date = date;
        this.startTime = startTime;
        this.endTime = endTime;
        this.locationAddress = locationAddress;
        this.imageUrl = imageUrl;
    }
}
