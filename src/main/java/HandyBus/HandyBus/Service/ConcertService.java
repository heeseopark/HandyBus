package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.ConcertDTO;
import HandyBus.HandyBus.DTO.ConcertSignUpDTO;

import java.util.List;

public interface ConcertService {

    ConcertDTO createConcert(ConcertSignUpDTO concert);

    List<ConcertDTO> findAll();

}
