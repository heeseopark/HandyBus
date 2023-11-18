package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.IdolDTO;

import java.util.List;

public interface IdolService {
    IdolDTO createIdol(IdolDTO.SignUp idol);
    List<IdolDTO> findAll();
    // IdolDTO updateIdol(IdolDTO idolDto);
    // void deleteIdol(Long id);
}
