package HandyBus.HandyBus.NewDTO;

import HandyBus.HandyBus.Domain.UserDomain;
import HandyBus.HandyBus.Domain.Subclass.Gender;
import lombok.Getter;
import lombok.Builder;

@Getter
public class UserDTO {

    private Long userId;
    private String name;
    private String email;
    private int phoneNumber;
    private String postCode;
    private Gender gender;

    // UserDomain에서 UserDTO로 변환
    public static UserDTO toDTO(UserDomain user) {
        return UserDTO.builder()
                .userId(user.getUserId())
                .name(user.getName())
                .email(user.getEmail())
                .phoneNumber(user.getPhoneNumber())
                .postCode(user.getPostCode())
                .gender(user.getGender())
                .build();
    }

    // 사용자 가입을 위한 Request DTO
    @Getter
    @Builder
    public static class SignUpRequest {
        private String email;
        private String name;
        private String password;
        private String phoneNumber;
        private String postCode;
        private Gender gender;

        // DTO에서 UserDomain으로의 변환
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

    // 사용자 가입을 위한 Response DTO
    @Getter
    @Builder
    public static class SignUpResponse {
        private String name;

        // 생성자, getter 등...
    }
}
