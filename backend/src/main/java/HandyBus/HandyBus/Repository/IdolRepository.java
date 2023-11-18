package HandyBus.HandyBus.Repository;

import HandyBus.HandyBus.Domain.IdolDomain;
import org.springframework.data.jpa.repository.JpaRepository;

public interface IdolRepository extends JpaRepository<IdolDomain, Long> {
}
