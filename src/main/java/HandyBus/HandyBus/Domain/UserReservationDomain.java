package HandyBus.HandyBus.Domain;

import jakarta.persistence.*;

import java.util.List;

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
    private ReservationDomain reservaion;

    @Column(nullable = false)
    private Boolean hasPaid;

    // Constructors, getters and setters
}