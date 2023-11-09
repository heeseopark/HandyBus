package HandyBus.HandyBus.Controller.Admin;

import HandyBus.HandyBus.DTO.ConcertDTO;
import HandyBus.HandyBus.DTO.IdolDTO;
import HandyBus.HandyBus.Service.ConcertServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/admin/concerts")
public class AdminConcertController {

    private final ConcertServiceImpl concertServiceImpl;

    @Autowired
    public AdminConcertController(ConcertServiceImpl concertServiceImpl) {
        this.concertServiceImpl = concertServiceImpl;
    }

    @GetMapping
    public ResponseEntity<List<ConcertDTO>> getConcertList() {
        List<ConcertDTO> concertList = concertServiceImpl.getAll(); // This should call your service layer to get the list
        return new ResponseEntity<>(concertList, HttpStatus.OK);
    }

    @GetMapping("/signup")
    public ResponseEntity<List<IdolDTO>> getIdolList(){

    }

    @PostMapping("/signup")
    public ResponseEntity<?> createConcert(@RequestBody ConcertDTO concertDTO) {
        // The service method 'createConcert' would handle saving the concert data
        // and possibly return the created concert object or any other confirmation details.
        ConcertDTO createdConcert = concertServiceImpl.createConcert(concertDTO);

        // Return a ResponseEntity with appropriate status (CREATED) and body
        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(createdConcert); // Or return just a header if no body is needed
    }

}
