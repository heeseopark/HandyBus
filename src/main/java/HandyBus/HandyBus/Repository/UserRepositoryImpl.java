package HandyBus.HandyBus.Repository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

@Repository
public class UserRepositoryImpl implements UserRepository{
    private final UserRepositoryImpl userRepositoryImpl;

    @Autowired
    public UserRepositoryImpl(UserRepositoryImpl userRepositoryImpl) {
        this.userRepositoryImpl = userRepositoryImpl;
    }

    // Additional methods for user operations can be added here
}
