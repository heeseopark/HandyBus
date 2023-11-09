package HandyBus.HandyBus.Controller.Admin;

import HandyBus.HandyBus.DTO.IdolDTO;
import HandyBus.HandyBus.Service.ConcertServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/admin/concertsignup")
public class AdminConcertController {

    private final ConcertServiceImpl concertServiceImpl;

    @Autowired
    public AdminConcertController(ConcertServiceImpl concertServiceImpl){
        this.concertServiceImpl = concertServiceImpl;
    }

    @GetMapping
    public ResponseEntity<List<IdolDTO>> getIdolList(){

    }

}
