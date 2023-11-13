package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.ConcertSignUpDTO;

import java.util.List;

public interface ConcertService {

    ConcertSignUpDTO createConcert(ConcertSignUpDTO concert);

    List<ConcertSignUpDTO> findAll();

}
