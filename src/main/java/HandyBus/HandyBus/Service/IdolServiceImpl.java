package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.ConcertSignUpDTO;
import HandyBus.HandyBus.DTO.IdolDTO;
import HandyBus.HandyBus.DTO.IdolSignUpDTO;
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

    private final ConcertServiceImpl concertService;

    @Autowired
    public IdolServiceImpl(IdolRepository idolRepository, ConcertServiceImpl concertService){
        this.idolRepository = idolRepository;
        this.concertService = concertService;
    }

    @Override
    public IdolSignUpDTO createIdol(IdolSignUpDTO idol) {

        IdolDomain createdIdol = idolRepository.save(toDomain(idol));

        return toSignUpDTO(createdIdol);
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

    //    public IdolDomain toDomain(IdolDTO idolDTO){
//
//        return IdolDomain.builder()
//                .name(idolDTO.getName())
//                .members(idolDTO.getMembers())
//                .concertList(idolDTO.getConcertList())
//                .build();

//    }

    private IdolDomain toDomain(IdolSignUpDTO idolSignUpDTO){

        return IdolDomain.builder()
                .name(idolSignUpDTO.getName())
                .members(idolSignUpDTO.getMembers())
                .build();
    }
    // idol service가 concert service를 주입 받아야하는게 마음에 들지는 않음. (dividing concerns)

    private IdolDTO toDTO(IdolDomain idolDomain) {
        List<ConcertSignUpDTO> concertSignUpDTOList = idolDomain.getConcertList().stream()
                .map(concertService::toSignUpDTO)
                .collect(Collectors.toList());

        return IdolDTO.builder()
                .name(idolDomain.getName())
                .members(idolDomain.getMembers())
                .concertList(concertSignUpDTOList)
                .build();
    }


    private IdolSignUpDTO toSignUpDTO(IdolDomain idolDomain){

        return IdolSignUpDTO.builder()
                .name(idolDomain.getName())
                .members(idolDomain.getMembers())
                .build();
    }
}
