package HandyBus.HandyBus.Controller.User;

import HandyBus.HandyBus.DTO.UserDTO;
import HandyBus.HandyBus.Service.UserServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("api/users"/)
public class UserController {

    private final UserServiceImpl userServiceImpl;

    @Autowired
    public UserController(UserServiceImpl userServiceImpl) {
        this.userServiceImpl = userServiceImpl;
    }

    @PostMapping("signup")
    public ResponseEntity<UserDTO> createUser(@RequestBody UserDTO.SignUpRequest user) {
        // The password hashing should be done inside the service layer, not exposed to the controller.

        UserDTO createdUser = userServiceImpl.createUser(user);
        return new ResponseEntity<>(createdUser, HttpStatus.CREATED);
    }

}
