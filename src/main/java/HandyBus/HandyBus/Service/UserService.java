package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.UserSignUpRequest;
import HandyBus.HandyBus.DTO.UserSignUpResponse;
import HandyBus.HandyBus.Domain.UserDomain;

import java.util.List;
import java.util.Optional;

public interface UserService {
    UserSignUpResponse createUser(UserSignUpRequest user);

    Optional<UserDomain> getUserById(Long id);

    List<UserDomain> getAllUsers();

    void deleteUser(Long id);

    UserDomain toDomain(UserSignUpRequest userSignUpRequest);

}
