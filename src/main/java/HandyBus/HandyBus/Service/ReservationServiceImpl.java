package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.ReservationDTO;
import HandyBus.HandyBus.DTO.ReservationSignUpRequestDTO;
import HandyBus.HandyBus.DTO.ReservationSignUpResponseDTO;
import HandyBus.HandyBus.Domain.ReservationDomain;
import HandyBus.HandyBus.Repository.ReservationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@Transactional
public class ReservationServiceImpl {

    private final ReservationRepository reservationRepository;

    @Autowired
    public ReservationServiceImpl(ReservationRepository reservationRepository){
        this.reservationRepository = reservationRepository;
    }

    @Override
    public ReservationSignUpResponseDTO createReservation(ReservationSignUpRequestDTO reservationSignUpRequestDTO){

        return ;
    }

    public List<ReservationDTO> getAll(){

        return ;
    }

    private ReservationDTO toDTO(ReservationDomain reservationDomain) {
        // Implement this method based on your fields in ReservationDomain and ReservationDTO
        return ReservationDTO.builder()
                .countRegistered(reservationDomain.getCountRegistered())
                .countPaid(reservationDomain.getCountPaid())
                .proceedStatus(reservationDomain.getProceedStatus())
                .build();
    }
}
