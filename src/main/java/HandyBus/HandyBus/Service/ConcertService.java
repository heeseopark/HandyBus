package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.ConcertDTO;
import HandyBus.HandyBus.Domain.ConcertDomain;

import java.util.List;

public interface ConcertService {

    ConcertDTO createConcert(ConcertDTO concert);

    List<ConcertDTO> getAll();

    ConcertDomain toDomain(ConcertDTO concertDTO);

    ConcertDTO toDTO(ConcertDomain concertDomain);
}
