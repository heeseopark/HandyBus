package HandyBus.HandyBus.Controller.User;

import HandyBus.HandyBus.DTO.UserSignUpRequest;
import HandyBus.HandyBus.DTO.UserSignUpResponse;
import HandyBus.HandyBus.Service.UserServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
public class UserController {

    private final UserServiceImpl userServiceImpl;

    @Autowired
    public UserController(UserServiceImpl userServiceImpl) {
        this.userServiceImpl = userServiceImpl;
    }

    @PostMapping
    public ResponseEntity<UserSignUpResponse> createUser(@RequestBody UserSignUpRequest userSignUpRequest) {
        // The password hashing should be done inside the service layer, not exposed to the controller.

        UserSignUpResponse newUser = userServiceImpl.createUser(userSignUpRequest);
        return new ResponseEntity<>(newUser, HttpStatus.CREATED);
    }

    // ... other REST endpoints ...
}
