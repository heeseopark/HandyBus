package HandyBus.HandyBus.DTO;

import lombok.Builder;
import lombok.Getter;

import java.util.List;

@Getter
@Builder
public class IdolSignUpDTO {

    private String name;
    private List<String> members;
}
