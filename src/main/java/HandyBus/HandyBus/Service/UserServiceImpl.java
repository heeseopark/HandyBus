package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.UserSignUpRequest;
import HandyBus.HandyBus.DTO.UserSignUpResponse;
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
    public UserSignUpResponse createUser(UserSignUpRequest user) {
        userRepository.save(toDomain(user));
        return UserSignUpResponse.builder()
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
    public UserDomain toDomain(UserSignUpRequest userSignUpRequest) {
        return UserDomain.builder()
                .email(userSignUpRequest.getEmail())
                .name(userSignUpRequest.getName())
                .passwordHash(passwordEncoder.encode(userSignUpRequest.getPassword()))
                .phoneNumber(Integer.parseInt(userSignUpRequest.getPhoneNumber()))
                .address(userSignUpRequest.getAddress())
                .gender(userSignUpRequest.getGender())
                .build();
    }


}
