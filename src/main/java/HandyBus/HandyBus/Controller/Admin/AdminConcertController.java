package HandyBus.HandyBus.Controller.Admin;

import HandyBus.HandyBus.DTO.ConcertSignUpDTO;
import HandyBus.HandyBus.DTO.IdolDTO;
import HandyBus.HandyBus.Service.ConcertServiceImpl;
import HandyBus.HandyBus.Service.IdolServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/admin")
public class AdminConcertController {

    private final ConcertServiceImpl concertServiceImpl;
    private final IdolServiceImpl idolServiceImpl;

    @Autowired
    public AdminConcertController(ConcertServiceImpl concertServiceImpl, IdolServiceImpl idolServiceImpl) {
        this.concertServiceImpl = concertServiceImpl;
        this.idolServiceImpl = idolServiceImpl;
    }

    @GetMapping //need to change this code
    public ResponseEntity<List<ConcertSignUpDTO>> getConcertAndReservationList() {
        List<ConcertSignUpDTO> concertList = concertServiceImpl.findUpcomingConcerts(); // This should call your service layer to get the list
        return new ResponseEntity<>(concertList, HttpStatus.OK);
    }

    @GetMapping("/concertsignup")
    public ResponseEntity<List<String>> getIdolNameList() {

        List<IdolDTO> idolDTOList = idolServiceImpl.findAllSorted();

        List<String> idolNameList = idolDTOList.stream()
                .map(IdolDTO::getName)
                .collect(Collectors.toList());

        return ResponseEntity.ok(idolNameList);
    }

    @PostMapping("/concertsignup")
    public ResponseEntity<Void> createConcert(@RequestBody ConcertSignUpDTO concertSignUpDTO) {

        concertServiceImpl.createConcert(concertSignUpDTO);

        return ResponseEntity.status(HttpStatus.OK).build();

        // if the front gets the ok status, redirect to the concert signup page
    }

    @GetMapping("/history")
    public ResponseEntity<List<ConcertSignUpDTO>> getAllConcerts() {
        List<ConcertSignUpDTO> allConcerts = concertServiceImpl.findAllSorted();
        return ResponseEntity.ok(allConcerts);
    }

    @DeleteMapping("/concert/{id}/delete")
    public ResponseEntity<Void> deleteConcert(@PathVariable Long id) {
        concertServiceImpl.deleteConcert(id);

        return ResponseEntity.status(HttpStatus.NO_CONTENT).build();
    }


}
