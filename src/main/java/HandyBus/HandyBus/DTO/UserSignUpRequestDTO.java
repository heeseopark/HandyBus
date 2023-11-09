package HandyBus.HandyBus.DTO;

import HandyBus.HandyBus.Domain.Subclass.Gender;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@NoArgsConstructor
@AllArgsConstructor
public class UserSignUpRequestDTO {

    private String email;
    private String name;
    private String password;
    private String phoneNumber;
    private String postCode;
    private Gender gender;

}

