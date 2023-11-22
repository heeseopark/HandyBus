package HandyBus.HandyBus.Controller.User;

import HandyBus.HandyBus.DTO.ReservationDTO;
import HandyBus.HandyBus.DTO.UserDTO;
import HandyBus.HandyBus.DTO.UserReservationDTO;
import HandyBus.HandyBus.Domain.UserReservationDomain;
import HandyBus.HandyBus.Service.ReservationServiceImpl;
import HandyBus.HandyBus.Service.UserReservationServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/reservations")
public class ReservationController {

    private final ReservationServiceImpl reservationService;
    private final UserReservationServiceImpl userReservationService;

    @Autowired
    public ReservationController(ReservationServiceImpl reservationService, UserReservationServiceImpl userReservationService){
        this.reservationService = reservationService;
        this.userReservationService = userReservationService;
    }

    @PostMapping("/signup")
    public ResponseEntity<Void> signUpReservation(UserDTO user, ReservationDTO reservation){

        if(user.getRegion().equals(reservation.getRegion())) {

            UserReservationDTO.SignUp userReservation = UserReservationDTO.SignUp.builder().userDTO(user).reservationDTO(reservation).hasPaid(null).build();

            userReservationService.createUserReservation(userReservation); // Assuming such a method exists

            return ResponseEntity.status(HttpStatus.CREATED).build();
        } else {
            // If regions do not match, return an error response
            return ResponseEntity.status(HttpStatus.FORBIDDEN).build();
        }
    }

}
