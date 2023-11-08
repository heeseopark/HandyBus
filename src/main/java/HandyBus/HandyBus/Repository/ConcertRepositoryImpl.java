package HandyBus.HandyBus.Repository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

@Repository
public class ConcertRepositoryImpl{

    private final ConcertRepository concertRepository;

    @Autowired
    public ConcertRepositoryImpl(ConcertRepository concertRepository) {
        this.concertRepository = concertRepository;
    }
}
