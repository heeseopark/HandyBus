package HandyBus.HandyBus.DTO;

import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@NoArgsConstructor
public class UserSignUpResponse {

    private String name;

    @Builder
    public UserSignUpResponse(String name){
        this.name = name;
    }

    // Constructors, getters, and setters
}
