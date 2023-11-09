package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.UserSignUpRequestDTO;
import HandyBus.HandyBus.DTO.UserSignUpResponseDTO;
import HandyBus.HandyBus.Domain.UserDomain;
import HandyBus.HandyBus.Repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
@Transactional
public class UserServiceImpl implements UserService {

    private final PasswordEncoder passwordEncoder;

    private final UserRepository userRepository;

    @Autowired
    public UserServiceImpl(UserRepository userRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    public UserSignUpResponseDTO createUser(UserSignUpRequestDTO user) {
        userRepository.save(toDomain(user));
        return UserSignUpResponseDTO.builder()
                .name(user.getName()).build();
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

    @Override
    public UserDomain toDomain(UserSignUpRequestDTO userSignUpRequestDTO) {
        return UserDomain.builder()
                .email(userSignUpRequestDTO.getEmail())
                .name(userSignUpRequestDTO.getName())
                .passwordHash(passwordEncoder.encode(userSignUpRequestDTO.getPassword()))
                .phoneNumber(Integer.parseInt(userSignUpRequestDTO.getPhoneNumber()))
                .address(userSignUpRequestDTO.getAddress())
                .gender(userSignUpRequestDTO.getGender())
                .build();
    }


}
