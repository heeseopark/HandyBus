package HandyBus.HandyBus.DTO;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

import java.util.List;

@AllArgsConstructor
@Builder
@Getter
public class IdolDTO {

    private String name;
    private List<String> members;
    private List<ConcertSignUpDTO> concertList;
}
