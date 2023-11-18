package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.UserDTO;
import HandyBus.HandyBus.Domain.UserDomain;
import HandyBus.HandyBus.Repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
@Transactional
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;


    @Autowired
    public UserServiceImpl(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    public UserDTO createUser(UserDTO.SignUpRequest user) {

        UserDomain createdUser = userRepository.save(user.toEntity());

        return UserDTO.toDTO(createdUser);
    }

    @Override
    public Optional<UserDomain> getUserById(Long id) {
        return userRepository.findById(id);
    }

    @Override
    public List<UserDomain> getAllUsers() {
        return userRepository.findAll();
    }

    @Override
    public void deleteUser(Long id) {
        userRepository.deleteById(id);
    }




}
