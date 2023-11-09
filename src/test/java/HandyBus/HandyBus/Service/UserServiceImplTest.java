package HandyBus.HandyBus.Service;

import HandyBus.HandyBus.DTO.UserSignUpRequestDTO;
import HandyBus.HandyBus.DTO.UserSignUpResponseDTO;
import HandyBus.HandyBus.Domain.Subclass.Address;
import HandyBus.HandyBus.Domain.Subclass.Gender;
import HandyBus.HandyBus.Domain.UserDomain;
import HandyBus.HandyBus.Repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
public class UserServiceImplTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @InjectMocks
    private UserServiceImpl userService;

    private UserSignUpRequestDTO userSignUpRequestDTO;
    private UserDomain userDomain;
    private String encodedPassword = "encodedPassword";

    @BeforeEach
    void setUp() {
        Address testAddress = new Address(
                "1234 Test St",
                "Test City",
                "TS",
                "12345",
                "Test Country"
        );

        // Setup test data using constructor and the enum for gender
        userSignUpRequestDTO = new UserSignUpRequestDTO(
                "test@example.com",
                "Test User",
                "password123",
                "1234567890",
                testAddress,
                Gender.MALE // Using the enum here
        );

        // Domain object that should be returned after mapping, using constructor
        userDomain = new UserDomain(
                userSignUpRequestDTO.getEmail(),
                userSignUpRequestDTO.getName(),
                encodedPassword, // Mock the encoding
                Integer.parseInt(userSignUpRequestDTO.getPhoneNumber()),
                userSignUpRequestDTO.getAddress(), // Directly passing the Address object
                userSignUpRequestDTO.getGender() // Directly passing the Gender enum
        );
    }



    @Test
    void whenCreateUser_thenUserShouldBeCreated() {
        // Given
        when(passwordEncoder.encode(userSignUpRequestDTO.getPassword())).thenReturn(encodedPassword);
        when(userRepository.save(any(UserDomain.class))).thenReturn(userDomain);

        // When
        UserSignUpResponseDTO result = userService.createUser(userSignUpRequestDTO);

        // Then
        assertEquals(userSignUpRequestDTO.getName(), result.getName(), "The name in the response should match the request");
        // Further assertions can be made to ensure all fields are mapped correctly, if needed.
        // You might also want to verify the interaction with the mock objects if necessary.
    }
}