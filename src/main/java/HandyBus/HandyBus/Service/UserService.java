package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.UserDTO;
import HandyBus.HandyBus.Domain.UserDomain;

import java.util.List;
import java.util.Optional;

public interface UserService {
    UserDTO createUser(UserDTO.SignUpRequest user);

    Optional<UserDomain> getUserById(Long id);

    List<UserDomain> getAllUsers();

    void deleteUser(Long id);


}
