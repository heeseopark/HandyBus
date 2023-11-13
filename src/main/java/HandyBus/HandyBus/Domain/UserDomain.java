package HandyBus.HandyBus.Domain;

import HandyBus.HandyBus.Domain.Subclass.Region;
import HandyBus.HandyBus.Domain.Subclass.Gender;
import lombok.*;
import jakarta.persistence.*;

import java.util.List;

@NoArgsConstructor
@Entity
@Getter
@Table(name = "users")
public class UserDomain {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(unique = true)
    private String email;

    @Column(nullable = false)
    private String passwordHash;

    @Column(nullable = false)
    private int phoneNumber;

    @Column(nullable = false)
    private String postCode;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Region region;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Gender gender;

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<UserReservationDomain> userReservationList; // Assuming Reservation is an entity that references UserDomain


    @Builder
    public UserDomain(String name, String email, String passwordHash, int phoneNumber, String postCode, Region region, Gender gender){
        this.name = name;
        this.email = email;
        this.passwordHash = passwordHash;
        this.phoneNumber = phoneNumber;
        this.postCode = postCode;
        this.region = region;
        this.gender = gender;
    }

    // 이거 service나 repository 쪽으로 빼고 싶음.
    public Region returnRegion(String postcode) {
        int code = Integer.parseInt(postcode);

        // Define ranges for major regions
        // Note: These ranges are for illustrative purposes and may not be accurate.
        // You should replace these with the actual postal code ranges for each region.
        if (code >= 0 && code <= 9999) {
            return Region.SEOUL;
        } else if (code >= 46000 && code <= 49999) {
            return Region.BUSAN;
        } else if (code >= 41000 && code <= 43999) {
            return Region.DAEGU;
        } else if (code >= 34000 && code <= 35999) {
            return Region.DAEJEON;
        } else {
            return null;
        }
    }

    // Constructors, getters, and setters

}
