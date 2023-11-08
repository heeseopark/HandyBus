package HandyBus.HandyBus.Domain;

import HandyBus.HandyBus.Domain.Subclass.Address;
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

    @Embedded
    @Column(nullable = false)
    private Address address;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Gender gender;

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<ReservationDomain> reservationList; // Assuming Reservation is an entity that references UserDomain


    @Builder
    public UserDomain(String name, String email, String passwordHash, int phoneNumber, Address address, Gender gender){
        this.name = name;
        this.email = email;
        this.passwordHash = passwordHash;
        this.phoneNumber = phoneNumber;
        this.address = address;
        this.gender = gender;
    }

    // Constructors, getters, and setters

}
