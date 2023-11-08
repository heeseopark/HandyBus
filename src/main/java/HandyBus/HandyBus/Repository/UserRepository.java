package HandyBus.HandyBus.Repository;

import HandyBus.HandyBus.Domain.UserDomain;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

public interface UserRepository extends JpaRepository<UserDomain, Long> {
    // Custom database queries can be added here
}
