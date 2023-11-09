package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.UserSignUpRequestDTO;
import HandyBus.HandyBus.DTO.UserSignUpResponseDTO;
import HandyBus.HandyBus.Domain.UserDomain;

import java.util.List;
import java.util.Optional;

public interface UserService {
    UserSignUpResponseDTO createUser(UserSignUpRequestDTO user);

    Optional<UserDomain> getUserById(Long id);

    List<UserDomain> getAllUsers();

    void deleteUser(Long id);

    UserDomain toDomain(UserSignUpRequestDTO userSignUpRequestDTO);

}
