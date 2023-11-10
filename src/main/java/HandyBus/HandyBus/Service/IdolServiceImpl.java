package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.IdolDTO;
import HandyBus.HandyBus.DTO.IdolSignUpDTO;
import HandyBus.HandyBus.Domain.IdolDomain;
import HandyBus.HandyBus.Repository.IdolRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
public class IdolServiceImpl implements IdolService{

    private final IdolRepository idolRepository;

    @Autowired
    public IdolServiceImpl(IdolRepository idolRepository){
        this.idolRepository = idolRepository;
    }

    @Override
    public IdolSignUpDTO createIdol(IdolSignUpDTO idol) {

        IdolDomain createdIdol = idolRepository.save(toDomain(idol));

        return toSignUpDTO(createdIdol);
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

//    public IdolDTO toDTO(IdolDomain idolDomain){
//
//        return IdolDTO.builder()
//                .name(idolDomain.getName())
//                .members(idolDomain.getMembers())
//                .concertList(idolDomain.getConcertList())
//                .build();
//    }

    private IdolSignUpDTO toSignUpDTO(IdolDomain idolDomain){

        return IdolSignUpDTO.builder()
                .name(idolDomain.getName())
                .members(idolDomain.getMembers())
                .build();
    }

}
