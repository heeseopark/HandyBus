package HandyBus.HandyBus.Service;

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
    public ConcertSignUpDTO createConcert(ConcertSignUpDTO concert){

        ConcertDomain createdConcert = concertRepository.save(toDomain(concert));

        return ConcertSignUpDTO.builder()
                .id(createdConcert.getId())
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

    public List<ConcertSignUpDTO> findUpcomingConcerts() {
        LocalDate today = LocalDate.now(); // Get the current date

        return concertRepository.findAll().stream()
                .filter(concert -> concert.getDate().isAfter(today)) // Filter concerts with a date after today
                .map(this::toSignUpDTO) // Convert to ConcertSignUpDTO
                .collect(Collectors.toList());
    }

    public List<ConcertSignUpDTO> findAllSorted() {
        return concertRepository.findAll().stream()
                .sorted(Comparator.comparing(ConcertDomain::getDate)
                        .thenComparing(ConcertDomain::getName))
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

    public ConcertSignUpDTO toSignUpDTO(ConcertDomain concertDomain){

        return ConcertSignUpDTO.builder()
                .id(concertDomain.getId())
                .name(concertDomain.getName())
                .date((concertDomain.getDate()))
                .startTime((concertDomain.getStartTime()))
                .endTime((concertDomain.getEndTime()))
                .location((concertDomain.getLocationAddress()))
                .build();
    }

    public void deleteConcert(Long id) {
        concertRepository.deleteById(id); // Assuming deleteById method is available in your repository
    }
}
