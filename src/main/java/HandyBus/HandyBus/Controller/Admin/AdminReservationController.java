package HandyBus.HandyBus.Controller.Admin;

import HandyBus.HandyBus.DTO.ConcertDTO;
import HandyBus.HandyBus.DTO.ConcertSignUpDTO;
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

    @GetMapping
    public ResponseEntity<List<ConcertDTO>> getConcerts(){

        List<ConcertDTO> concertList = concertServiceImpl.findUpcomingConcerts();

        return new ResponseEntity<>(concertList, HttpStatus.OK);
    }


    @PostMapping
    public ResponseEntity<?> createReservation(@RequestBody ReservationSignUpRequestDTO reservationSignUpRequestDTO){

        reservationServiceImpl.createReservation(reservationSignUpRequestDTO);

        return ResponseEntity.status(HttpStatus.CREATED).build();
    }
}
