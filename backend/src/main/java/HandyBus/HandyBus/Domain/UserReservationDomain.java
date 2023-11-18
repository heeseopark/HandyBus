package HandyBus.HandyBus.Domain;

import jakarta.persistence.*;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.apache.catalina.User;

import java.util.List;

@Entity
@Getter
@NoArgsConstructor
public class UserReservationDomain {

    // cascade 설정 고민하기

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long userReservationId;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private UserDomain user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "reservation_id")
    private ReservationDomain reservation;

    @Column(nullable = false)
    private Boolean hasPaid;

    @Builder
    public UserReservationDomain(UserDomain user, ReservationDomain reservation, Boolean hasPaid){
        this.user = user;
        this.reservation = reservation;
        this.hasPaid = hasPaid;
    }
}