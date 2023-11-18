package HandyBus.HandyBus.DTO;

import HandyBus.HandyBus.Domain.UserReservationDomain;
import lombok.Builder;

@Builder
public class UserReservationDTO {

    private Long userReservationId;
    private UserDTO userDTO;
    private ReservationDTO reservationDTO;
    private Boolean hasPaid;

    public static UserReservationDTO toDTO(UserReservationDomain userReservation){
        return UserReservationDTO.builder()
                .userReservationId(userReservation.getUserReservationId())
                .userDTO(UserDTO.toDTO(userReservation.getUser()))
                .reservationDTO(ReservationDTO.toDTO(userReservation.getReservation()))
                .hasPaid(userReservation.getHasPaid())
                .build();
    }

    public UserReservationDomain toEntity(){
        return UserReservationDomain.builder()
                .user(this.userDTO.toEntity())
                .reservation(this.reservationDTO.toEntity())
                .hasPaid(this.hasPaid)
                .build();
    }

    @Builder
    public static class SignUp {

        private UserDTO userDTO;
        private ReservationDTO reservationDTO;
        private Boolean hasPaid;

        public UserReservationDomain toEntity() {
            return UserReservationDomain.builder()
                    .user(this.userDTO.toEntity())
                    .reservation(this.reservationDTO.toEntity())
                    .hasPaid(this.hasPaid)
                    .build();
        }
    }

}
