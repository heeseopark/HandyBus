package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.UserReservationDTO;
import HandyBus.HandyBus.Domain.UserReservationDomain;
import HandyBus.HandyBus.Repository.UserReservationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
public class UserReservationServiceImpl implements UserReservationService{

    private final UserReservationRepository userReservationRepository;

    @Autowired
    public UserReservationServiceImpl(UserReservationRepository userReservationRepository){
        this.userReservationRepository = userReservationRepository;
    }

    @Override
    public UserReservationDTO createUserReservation(UserReservationDTO.SignUp userReservation){
        UserReservationDomain createdUserReservation = userReservationRepository.save(userReservation.toEntity());
        return UserReservationDTO.toDTO(createdUserReservation);
    }

}
