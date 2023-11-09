package HandyBus.HandyBus.Repository;

import HandyBus.HandyBus.Domain.ReservationDomain;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ReservationRepository extends JpaRepository<ReservationDomain, Long> {
}
