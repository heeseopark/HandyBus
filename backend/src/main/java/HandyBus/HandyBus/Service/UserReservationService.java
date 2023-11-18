package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.UserReservationDTO;
import HandyBus.HandyBus.Domain.UserReservationDomain;

public interface UserReservationService {

    UserReservationDTO createUserReservation(UserReservationDTO.SignUp userReservation);

}
