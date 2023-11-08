package HandyBus.HandyBus.Controller.Admin;

import HandyBus.HandyBus.DTO.ConcertSignUpDTO;
import HandyBus.HandyBus.Service.ConcertServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/admin/concerts")
public class AdminConcertController {

    private final ConcertServiceImpl concertServiceImpl;

    @Autowired
    public AdminConcertController(ConcertServiceImpl concertServiceImpl) {
        this.concertServiceImpl = concertServiceImpl;
    }

    @PostMapping("/signup")
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
