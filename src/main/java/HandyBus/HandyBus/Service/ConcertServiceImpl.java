package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.ConcertSignUpDTO;
import HandyBus.HandyBus.Repository.ConcertRepositoryImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
public class ConcertServiceImpl implements ConcertService{

    private final ConcertRepositoryImpl concertServiceImpl;

    @Autowired
    public ConcertServiceImpl(ConcertRepositoryImpl concertRepositoryImpl){
        this.concertServiceImpl = concertRepositoryImpl;
    }

    @Override
    public ConcertSignUpDTO createConcert(ConcertSignUpDTO concert){

        // fill this code

        return concert;
    }
}
