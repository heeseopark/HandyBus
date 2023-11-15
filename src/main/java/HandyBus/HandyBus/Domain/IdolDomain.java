package HandyBus.HandyBus.Domain;

import jakarta.persistence.*;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.List;

@Entity
@Getter
@NoArgsConstructor
public class IdolDomain {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long idolId;

    private String name;

    @ElementCollection
    private List<String> members = new ArrayList<>();

    @OneToMany(mappedBy = "idol", cascade = CascadeType.ALL)
    private List<ConcertDomain> concertList = new ArrayList<>();

    @Builder
    public IdolDomain(String name, List<String> members, List<ConcertDomain> concertList){
        this.name = name;
        this.members = members;
        this.concertList = concertList;
    }

}