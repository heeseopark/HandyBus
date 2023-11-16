package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.ConcertDTO;
import HandyBus.HandyBus.DTO.ConcertSignUpDTO;
import HandyBus.HandyBus.DTO.IdolDTO;
import HandyBus.HandyBus.DTO.IdolSignUpDTO;
import HandyBus.HandyBus.Domain.ConcertDomain;
import HandyBus.HandyBus.Domain.IdolDomain;
import HandyBus.HandyBus.Repository.IdolRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional
public class IdolServiceImpl implements IdolService{

    private final IdolRepository idolRepository;

    private final ConcertServiceImpl concertServiceImpl;

    @Autowired
    public IdolServiceImpl(IdolRepository idolRepository, ConcertServiceImpl concertServiceImpl){
        this.idolRepository = idolRepository;
        this.concertServiceImpl = concertServiceImpl;
    }

    @Override
    public IdolDTO createIdol(IdolSignUpDTO idolSignUpDTO) {

        IdolDomain createdIdol = idolRepository.save(toDomain(idolSignUpDTO));

        return toDTO(createdIdol);
    }

    @Override
    public List<IdolDTO> findAll() {

        return idolRepository.findAll().stream()
                .map(this::toDTO)
                .collect(Collectors.toList());
    }

    public List<IdolDTO> findAllSorted() {
        return idolRepository.findAll().stream()
                .map(this::toDTO) // Convert each IdolDomain to IdolDTO
                .sorted(Comparator.comparingInt((IdolDTO idol) -> idol.getConcertList().size())
                        .thenComparing(IdolDTO::getName))
                .collect(Collectors.toList());
    }


}
