package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.ConcertSignUpDTO;
import HandyBus.HandyBus.Domain.ConcertDomain;
import HandyBus.HandyBus.Repository.ConcertRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional
public class ConcertServiceImpl implements ConcertService{

    private final ConcertRepository concertRepository;

    @Autowired
    public ConcertServiceImpl(ConcertRepository concertRepository){
        this.concertRepository = concertRepository;
    }

    @Override
    public ConcertSignUpDTO createConcert(ConcertSignUpDTO concert){

        ConcertDomain createdConcert = concertRepository.save(toDomain(concert));

        return ConcertSignUpDTO.builder()
                .name(createdConcert.getName())
                .date(createdConcert.getDate())
                .startTime(createdConcert.getStartTime())
                .endTime((createdConcert.getEndTime()))
                .location(createdConcert.getLocationAddress())
                .build();
    }

    @Override
    public List<ConcertSignUpDTO> findAll() {
        return concertRepository.findAll().stream()
                .map(this::toSignUpDTO)
                .collect(Collectors.toList());
    }


    private ConcertDomain toDomain(ConcertSignUpDTO concertSignUpDTO){

        return ConcertDomain.builder()
                .name(concertSignUpDTO.getName())
                .date(concertSignUpDTO.getDate())
                .startTime(concertSignUpDTO.getStartTime())
                .endTime((concertSignUpDTO.getEndTime()))
                .locationAddress(concertSignUpDTO.getLocation())
                .imageUrl(concertSignUpDTO.getImageUrl())
                .build();
    }

    private ConcertSignUpDTO toSignUpDTO(ConcertDomain concertDomain){

        return ConcertSignUpDTO.builder()
                .name(concertDomain.getName())
                .date((concertDomain.getDate()))
                .startTime((concertDomain.getStartTime()))
                .endTime((concertDomain.getEndTime()))
                .location((concertDomain.getLocationAddress()))
                .build();
    }
}
