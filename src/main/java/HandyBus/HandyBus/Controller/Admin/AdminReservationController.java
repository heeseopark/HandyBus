package HandyBus.HandyBus.Controller.Admin;

import HandyBus.HandyBus.DTO.ConcertDTO;
import HandyBus.HandyBus.DTO.ReservationSignUpRequestDTO;
import HandyBus.HandyBus.DTO.ReservationSignUpResponseDTO;
import HandyBus.HandyBus.Service.ConcertServiceImpl;
import HandyBus.HandyBus.Service.ReservationServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("admin/reservationsignup")
public class AdminReservationController {

    private final ReservationServiceImpl reservationServiceImpl;
    private final ConcertServiceImpl concertServiceImpl;

    @Autowired
    public AdminReservationController(ReservationServiceImpl reservationServiceImpl, ConcertServiceImpl concertServiceImpl){
        this.reservationServiceImpl = reservationServiceImpl;
        this.concertServiceImpl = concertServiceImpl;
    }


    @PostMapping("/signup")
    public ResponseEntity<ReservationSignUpResponseDTO> createReservation(@RequestBody ReservationSignUpRequestDTO reservationSignUpRequestDTO){

        ReservationSignUpResponseDTO newReservation = reservationServiceImpl.createReservation(reservationSignUpRequestDTO);

        return new ResponseEntity<>(newReservation, HttpStatus.CREATED);
    }
}
