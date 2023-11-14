package HandyBus.HandyBus.Domain;

import jakarta.persistence.*;
import lombok.Builder;
import lombok.Getter;

import java.util.ArrayList;
import java.util.List;

@Entity
@Getter
public class IdolDomain {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;

    @ElementCollection
    private List<String> members = new ArrayList<>(); // Assuming members are stored as a list of strings

    @OneToMany(mappedBy = "idol", cascade = CascadeType.ALL)
    private List<ConcertDomain> concertList = new ArrayList<>();

    @Builder
    public IdolDomain(String name, List<String> members, List<ConcertDomain> concertList){
        this.name = name;
        this.members = members;
        this.concertList = concertList;
    }

}