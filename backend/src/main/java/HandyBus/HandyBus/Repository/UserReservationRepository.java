package HandyBus.HandyBus.Repository;

import HandyBus.HandyBus.Domain.UserReservationDomain;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserReservationRepository extends JpaRepository<UserReservationDomain, Long> {
}
