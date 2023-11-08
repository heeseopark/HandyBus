package HandyBus.HandyBus.Repository;

import HandyBus.HandyBus.Domain.ConcertDomain;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ConcertRepository extends JpaRepository<ConcertDomain, Long> {
}
