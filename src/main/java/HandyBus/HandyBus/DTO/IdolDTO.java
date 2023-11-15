package HandyBus.HandyBus.DTO;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

import java.util.List;

@AllArgsConstructor
@Builder
@Getter
public class IdolDTO {

    private Long idolId;
    private String name;
    private List<String> members;
    private List<ConcertDTO> concertList;
}
