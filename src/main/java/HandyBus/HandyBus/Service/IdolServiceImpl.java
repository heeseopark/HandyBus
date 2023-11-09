package HandyBus.HandyBus.Service;

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


}
