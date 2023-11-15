package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.ConcertDTO;
import HandyBus.HandyBus.DTO.ConcertSignUpDTO;
import HandyBus.HandyBus.Domain.ConcertDomain;
import HandyBus.HandyBus.Repository.ConcertRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.Comparator;
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
    public ConcertDTO createConcert(ConcertSignUpDTO concert){

        ConcertDomain createdConcert = concertRepository.save(toDomain(concert));

        return ConcertDTO.builder()
                .concertId(createdConcert.getConcertId())
                .name(createdConcert.getName())
                .date(createdConcert.getDate())
                .startTime(createdConcert.getStartTime())
                .endTime((createdConcert.getEndTime()))
                .location(createdConcert.getLocationAddress())
                .imageUrl(createdConcert.getImageUrl())
                .build();
    }

    @Override
    public List<ConcertDTO> findAll() {
        return concertRepository.findAll().stream()
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    public List<ConcertDTO> findUpcomingConcerts() {
        LocalDate today = LocalDate.now(); // Get the current date

        return concertRepository.findAll().stream()
                .filter(concert -> concert.getDate().isAfter(today)) // Filter concerts with a date after today
                .map(this::toDTO) // Convert to ConcertSignUpDTO
                .collect(Collectors.toList());
    }

    public List<ConcertDTO> findAllSorted() {
        return concertRepository.findAll().stream()
                .sorted(Comparator.comparing(ConcertDomain::getDate)
                        .thenComparing(ConcertDomain::getName))
                .map(this::toDTO)
                .collect(Collectors.toList());

    }

    protected ConcertDomain toDomain(ConcertDTO concertDTO){

        return ConcertDomain.builder()
                .name(concertDTO.getName())
                .date(concertDTO.getDate())
                .startTime(concertDTO.getStartTime())
                .endTime((concertDTO.getEndTime()))
                .locationAddress(concertDTO.getLocation())
                .imageUrl(concertDTO.getImageUrl())
                .build();
    }

    protected ConcertDomain toDomain(ConcertSignUpDTO concertSignUpDTO){

        return ConcertDomain.builder()
                .name(concertSignUpDTO.getName())
                .date(concertSignUpDTO.getDate())
                .startTime(concertSignUpDTO.getStartTime())
                .endTime((concertSignUpDTO.getEndTime()))
                .locationAddress(concertSignUpDTO.getLocation())
                .imageUrl(concertSignUpDTO.getImageUrl())
                .build();
    }

    protected ConcertDTO toDTO(ConcertDomain concertDomain){

        return ConcertDTO.builder()
                .concertId(concertDomain.getConcertId())
                .name(concertDomain.getName())
                .date((concertDomain.getDate()))
                .startTime((concertDomain.getStartTime()))
                .endTime((concertDomain.getEndTime()))
                .location((concertDomain.getLocationAddress()))
                .build();
    }

    public void deleteConcert(Long id) {
        concertRepository.deleteById(id);
    }
}
