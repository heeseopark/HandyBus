package HandyBus.HandyBus.DTO;

import HandyBus.HandyBus.Domain.Subclass.ProceedStatus;
import lombok.Builder;

@Builder
public class ReservationDTO {

    private int countRegistered;
    private int countPaid;
    private ProceedStatus proceedStatus;
}
