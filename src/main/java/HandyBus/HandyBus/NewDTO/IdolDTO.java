package HandyBus.HandyBus.NewDTO;

import HandyBus.HandyBus.Domain.ConcertDomain;
import HandyBus.HandyBus.Domain.IdolDomain;
import lombok.Builder;
import lombok.Getter;

import java.util.List;
import java.util.stream.Collectors;

@Builder
@Getter
public class IdolDTO {

    private Long idolId;
    private String name;
    private List<String> members;
    private List<ConcertDTO> concertList;

    public static IdolDTO toDTO(IdolDomain idol) {
        return IdolDTO.builder()
                .idolId(idol.getIdolId())
                .name(idol.getName())
                .members(idol.getMembers())
                .concertList(idol.getConcertList().stream().map(ConcertDTO::toDTO).collect(Collectors.toList()))
                .build();
    }

    @Getter
    public static class SignUp {
        private String name;
        private List<String> members;


        public IdolDomain toEntity() {
            return IdolDomain.builder()
                    .name(this.name)
                    .members(this.members)
                    .build();
        }
    }

}
