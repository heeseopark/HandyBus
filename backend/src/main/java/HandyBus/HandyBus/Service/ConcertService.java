package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.ConcertDTO;

import java.util.List;

public interface ConcertService {

    ConcertDTO createConcert(ConcertDTO.SignUp concert);

    List<ConcertDTO> findAll();

}
