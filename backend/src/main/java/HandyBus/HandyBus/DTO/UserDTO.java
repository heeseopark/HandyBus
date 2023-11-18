package HandyBus.HandyBus.DTO;

import HandyBus.HandyBus.Domain.Subclass.Region;
import HandyBus.HandyBus.Domain.UserDomain;
import HandyBus.HandyBus.Domain.Subclass.Gender;
import HandyBus.HandyBus.Domain.UserReservationDomain;
import lombok.Getter;
import lombok.Builder;

import java.util.List;
import java.util.stream.Collectors;

@Getter
@Builder
public class UserDTO {

    private Long userId;
    private String name;
    private String email;
    private int phoneNumber;
    private String postCode;
    private Region region;
    private Gender gender;
    private List<UserReservationDTO> userReservationList;

    public static UserDTO toDTO(UserDomain user) {
        return UserDTO.builder()
                .userId(user.getUserId())
                .name(user.getName())
                .email(user.getEmail())
                .phoneNumber(user.getPhoneNumber())
                .region(user.getRegion())
                .phoneNumber(user.getPhoneNumber())
                .postCode(user.getPostCode())
                .gender(user.getGender())
                .userReservationList(user.getUserReservationList().stream().map(UserReservationDTO::toDTO).collect(Collectors.toList()))
                .build();
    }

    public UserDomain toEntity(){
        return UserDomain.builder()
                .name(this.name)
                .email(this.email)
                .phoneNumber(this.phoneNumber)
                .postCode(this.postCode)
                .region(this.region)
                .gender(this.gender)
                .userReservationList(this.userReservationList.stream().map(UserReservationDTO::toEntity).collect(Collectors.toList()))
                .build();
    }

    @Builder
    public static class SignUpRequest {
        private String email;
        private String name;
        private String password;
        private String phoneNumber;
        private String postCode;
        private Gender gender;

        public UserDomain toEntity() {
            return UserDomain.builder()
                    .name(this.name)
                    .email(this.email)
                    .passwordHash(this.password) // 여기서 비밀번호 해싱이 필요할 수 있음
                    .phoneNumber(Integer.parseInt(this.phoneNumber))
                    .postCode(this.postCode)
                    .gender(this.gender)
                    .build();
        }
    }

    @Builder
    public static class SignUpResponse {
        private String name;


    }
}
