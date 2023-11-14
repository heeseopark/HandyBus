package HandyBus.HandyBus.Domain;

import jakarta.persistence.*;

import java.util.List;

@Entity
public class UserReservationDomain {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private UserDomain user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "reservation_id")
    private ReservationDomain reservation;

    @Column(nullable = false)
    private Boolean hasPaid;

    // Constructors, getters and setters
}