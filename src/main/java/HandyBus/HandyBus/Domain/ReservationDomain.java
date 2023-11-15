package HandyBus.HandyBus.Domain;

import HandyBus.HandyBus.Domain.Subclass.ProceedStatus;
import jakarta.persistence.*;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@Getter
@NoArgsConstructor
public class ReservationDomain {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long reservationId; // Assuming there is an ID field

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "concert_id")
    private ConcertDomain concert; // Relation to ConcertDomain

    @OneToMany(mappedBy = "busId")
    private List<BusDomain> busList = new ArrayList<>(); // One-to-many relationship with BusDomain

    @OneToMany(mappedBy = "reservation")
    private List<UserReservationDomain> userReservationList = new ArrayList<>();

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

    private String imageUrl;

    @Builder
    public ReservationDomain(ConcertDomain concert, List<BusDomain> busList,
                             List<UserReservationDomain> userReservationList,
                             LocalDateTime requiredArriveTime, ProceedStatus proceedStatus,
                             int price, String qrImage, String chatRoomUrl, String imageUrl) {
        this.concert = concert;
        this.busList = busList;
        this.userReservationList = userReservationList;
        this.requiredArriveTime = requiredArriveTime;
        this.proceedStatus = proceedStatus;
        this.price = price;
        this.qrImage = qrImage;
        this.chatRoomUrl = chatRoomUrl;
        this.imageUrl = imageUrl;
    }



}
