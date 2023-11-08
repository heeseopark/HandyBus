package HandyBus.HandyBus.DTO;

import HandyBus.HandyBus.Domain.Subclass.Address;
import HandyBus.HandyBus.Domain.Subclass.Gender;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@NoArgsConstructor
public class UserSignUpRequest {

    private String email;
    private String name;
    private String password;
    private String phoneNumber;
    private Address address;
    private Gender gender;

}

