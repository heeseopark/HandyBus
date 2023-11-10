package HandyBus.HandyBus.Domain;

import jakarta.persistence.*;

@Entity
public class UserReservationDomain {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private UserDomain user;

    @ManyToOne
    @JoinColumn(name = "reservation_id")
    private ReservationDomain reservation;

    @Column(nullable = false)
    private Boolean hasPaid;

    // Constructors, getters and setters
}