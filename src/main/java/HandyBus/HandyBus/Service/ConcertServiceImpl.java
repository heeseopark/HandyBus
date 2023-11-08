package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.ConcertSignUpDTO;
import HandyBus.HandyBus.Repository.ConcertRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

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

        // fill this code

        return concert;
    }
}
