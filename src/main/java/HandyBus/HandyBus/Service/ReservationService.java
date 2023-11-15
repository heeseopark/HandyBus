package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.ReservationSignUpRequestDTO;
import HandyBus.HandyBus.DTO.ReservationSignUpResponseDTO;

public interface ReservationService {

    ReservationSignUpResponseDTO createReservation(ReservationSignUpRequestDTO reservationSignUpRequestDTO);

}
