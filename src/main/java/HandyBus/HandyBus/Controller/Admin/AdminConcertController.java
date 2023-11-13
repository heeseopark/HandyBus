package HandyBus.HandyBus.Controller.Admin;

import HandyBus.HandyBus.DTO.ConcertSignUpDTO;
import HandyBus.HandyBus.DTO.IdolDTO;
import HandyBus.HandyBus.Service.ConcertServiceImpl;
import HandyBus.HandyBus.Service.ReservationServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/admin")
public class AdminConcertController {

    private final ConcertServiceImpl concertServiceImpl;
    private final ReservationServiceImpl reservationServiceImpl;

    @Autowired
    public AdminConcertController(ConcertServiceImpl concertServiceImpl, ReservationServiceImpl reservationServiceImpl) {
        this.concertServiceImpl = concertServiceImpl;
        this.reservationServiceImpl = reservationServiceImpl;
    }

    @GetMapping //need to change this code
    public ResponseEntity<List<ConcertSignUpDTO>> getConcertAndReservationList() {
        List<ConcertSignUpDTO> concertList = concertServiceImpl.findAll(); // This should call your service layer to get the list
        return new ResponseEntity<>(concertList, HttpStatus.OK);
    }

    @GetMapping("/concertsignup")
    public ResponseEntity<List<IdolDTO>> getIdolList(){

    }

    @PostMapping("/concertsignup")
    public ResponseEntity<?> createConcert(@RequestBody ConcertSignUpDTO concertSignUpDTO) {
        // The service method 'createConcert' would handle saving the concert data
        // and possibly return the created concert object or any other confirmation details.
        ConcertSignUpDTO createdConcert = concertServiceImpl.createConcert(concertSignUpDTO);

        // Return a ResponseEntity with appropriate status (CREATED) and body
        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(createdConcert); // Or return just a header if no body is needed
    }

}
