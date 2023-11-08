package HandyBus.HandyBus.Domain;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.List;

@Entity
public class ReservationDomain {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id; // Assuming there is an ID field

    @ManyToOne
    @JoinColumn(name = "concert_id")
    private ConcertDomain concertID; // Relation to ConcertDomain

    @OneToMany(mappedBy = "reservation")
    private List<BusDomain> busIDList; // One-to-many relationship with BusDomain

    @OneToMany(mappedBy = "reservation")
    private List<UserDomain> userList; // One-to-many relationship with UserDomain

    @Column(nullable = false)
    private LocalDateTime requiredArriveTime; // Using LocalDateTime for date-time fields

    @Enumerated(EnumType.STRING)
    private ProceedStatus proceedStatus; // Enum for status

    @Column(nullable = false)
    private int price; // Price field

    @Column(length = 500)
    private String qrImage; // URL field for QR image, length can be adjusted based on expected URL length

    @Column(length = 500)
    private String chatRoomUrl; // URL field for chat room

    // Getters and setters for all fields

    // ProceedStatus enum definition (assuming it's an inner enum, otherwise it could be in its own file)
    public enum ProceedStatus {
        PENDING,
        CONFIRMED,
        CANCELLED,
        COMPLETED
    }

    // Constructor, getters, and setters...
}
