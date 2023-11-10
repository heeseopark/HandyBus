package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.ConcertDTO;
import HandyBus.HandyBus.Domain.ConcertDomain;
import HandyBus.HandyBus.Repository.ConcertRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.ArrayList;
import java.util.List;

@Service
@Transactional
public class ConcertServiceImpl implements ConcertService{

    private final ConcertRepository concertRepository;

    @Autowired
    public ConcertServiceImpl(ConcertRepository concertRepository){
        this.concertRepository = concertRepository;
    }

    @Override
    public ConcertDTO createConcert(ConcertDTO concert){

        concertRepository.save(toDomain(concert));

        return ConcertDTO.builder()
                .name(concert.getName())
                .date(concert.getDate())
                .startTime(concert.getStartTime())
                .endTime((concert.getEndTime()))
                .location(concert.getLocation())
                .build();
    }

    @Override
    public List<ConcertDTO> findAll(){
        List<ConcertDTO> concertDTOList = new ArrayList<>();

        for (ConcertDomain concertDomain : concertRepository.findAll()){
            // consider sorting
            concertDTOList.add(toDTO(concertDomain));

        }

        return concertDTOList;
    }

    private ConcertDomain toDomain(ConcertDTO concert){

        return ConcertDomain.builder()
                .name(concert.getName())
                .date(concert.getDate())
                .startTime(concert.getStartTime())
                .endTime((concert.getEndTime()))
                .locationAddress(concert.getLocation())
                .build();
    }

    private ConcertDTO toDTO(ConcertDomain concertDomain){

        return ConcertDTO.builder()
                .name(concertDomain.getName())
                .date((concertDomain.getDate()))
                .startTime((concertDomain.getStartTime()))
                .endTime((concertDomain.getEndTime()))
                .location((concertDomain.getLocationAddress()))
                .build();
    }
}
