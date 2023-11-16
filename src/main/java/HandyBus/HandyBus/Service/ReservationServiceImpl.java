package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.ReservationDTO;
import HandyBus.HandyBus.Domain.ReservationDomain;
import HandyBus.HandyBus.Repository.ReservationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalTime;
import java.util.List;

@Service
@Transactional
public class ReservationServiceImpl implements ReservationService{

    private final ReservationRepository reservationRepository;

    @Autowired
    public ReservationServiceImpl(ReservationRepository reservationRepository){
        this.reservationRepository = reservationRepository;
    }

    @Override
    public ReservationDTO createReservation(ReservationDTO.SignUp reservation){

        ReservationDomain createdReservation = reservationRepository.save(reservation.toEntity());

        return ReservationDTO.toDTO(createdReservation);
    }


    public List<ReservationDTO> finAll(){

        return null;
    }


}
