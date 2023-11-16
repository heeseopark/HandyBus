package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.ConcertDTO;
import HandyBus.HandyBus.Domain.ConcertDomain;
import HandyBus.HandyBus.Repository.ConcertRepository;

import org.aspectj.weaver.patterns.ConcreteCflowPointcut;
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
    public ConcertDTO createConcert(ConcertDTO.SignUp concert){

        ConcertDomain createdConcert = concertRepository.save(concert.toEntity());

        return ConcertDTO.toDTO(createdConcert);
    }

    @Override
    public List<ConcertDTO> findAll() {
        return concertRepository.findAll().stream()
                .map(ConcertDTO::toDTO)
                .collect(Collectors.toList());
    }

    public List<ConcertDTO> findUpcomingConcerts() {
        LocalDate today = LocalDate.now(); // Get the current date

        return concertRepository.findAll().stream()
                .filter(concert -> concert.getDate().isAfter(today)) // Filter concerts with a date after today
                .map(ConcertDTO::toDTO) // Convert to ConcertSignUpDTO
                .collect(Collectors.toList());
    }

    public List<ConcertDTO> findAllSorted() {
        return concertRepository.findAll().stream()
                .sorted(Comparator.comparing(ConcertDomain::getDate)
                        .thenComparing(ConcertDomain::getName))
                .map(ConcertDTO::toDTO)
                .collect(Collectors.toList());

    }

    public void deleteConcert(Long id) {
        concertRepository.deleteById(id);
    }
}
