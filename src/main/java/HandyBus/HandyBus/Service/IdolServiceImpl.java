package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.IdolDTO;
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

    @Autowired
    public IdolServiceImpl(IdolRepository idolRepository){
        this.idolRepository = idolRepository;
    }

    @Override
    public IdolDTO createIdol(IdolDTO.SignUp idol) {

        IdolDomain createdIdol = idolRepository.save(idol.toEntity());

        return IdolDTO.toDTO(createdIdol);
    }

    @Override
    public List<IdolDTO> findAll() {

        return idolRepository.findAll().stream()
                .map(IdolDTO::toDTO)
                .collect(Collectors.toList());
    }

    public List<IdolDTO> findAllSorted() {
        return idolRepository.findAll().stream()
                .map(IdolDTO::toDTO)
                .sorted(Comparator.comparing(IdolDTO::getName))
                .collect(Collectors.toList());
    }



}
