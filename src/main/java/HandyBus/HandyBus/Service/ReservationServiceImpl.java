package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.ReservationDTO;
import HandyBus.HandyBus.DTO.ReservationSignUpRequestDTO;
import HandyBus.HandyBus.DTO.ReservationSignUpResponseDTO;
import HandyBus.HandyBus.Domain.ReservationDomain;
import HandyBus.HandyBus.Repository.ReservationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalTime;
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

        ReservationDomain createdReservation = reservationRepository.save(toDomain(reservationSignUpRequestDTO));

        // Build and return the response DTO
        return ReservationSignUpResponseDTO.builder()
                .concertId(createdReservation.getConcert().getConcertId()) // Assuming you want to return the concertId
                .requiredArriveTime(LocalTime.from(createdReservation.getRequiredArriveTime()))
                .qrImage(createdReservation.getQrImage())
                .chatRoomUrl(createdReservation.getChatRoomUrl())
                .imageUrl(createdReservation.getImageUrl())
                .build();
    }


    public List<ReservationDTO> getAll(){

        return null;
    }

//    private ReservationSignUpResponseDTO toResponseDTO(ReservationDomain reservationDomain) {
//        // Implement this method based on your fields in ReservationDomain and ReservationDTO
//        return ReservationDTO.builder()
//                .countRegistered(reservationDomain.getCountRegistered())
//                .countPaid(reservationDomain.getCountPaid())
//                .proceedStatus(reservationDomain.getProceedStatus())
//                .build();
//    }


}
