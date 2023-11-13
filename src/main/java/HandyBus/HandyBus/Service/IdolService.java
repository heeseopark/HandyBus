package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.IdolDTO;
import HandyBus.HandyBus.DTO.IdolSignUpDTO;

import java.util.List;

public interface IdolService {
    IdolSignUpDTO createIdol(IdolSignUpDTO idolSignUpDTO);
    List<IdolDTO> findAll();
    // IdolDTO updateIdol(IdolDTO idolDto);
    // void deleteIdol(Long id);
}
