package HandyBus.HandyBus.DTO;

import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@NoArgsConstructor
public class UserSignUpResponseDTO {

    private String name;

    @Builder
    public UserSignUpResponseDTO(String name){
        this.name = name;
    }

    // Constructors, getters, and setters
}
