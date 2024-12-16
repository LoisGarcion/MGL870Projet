package MicroUser.UserSpringBoot.Controller;

import MicroUser.UserSpringBoot.Dto.BuyRequestDto;
import MicroUser.UserSpringBoot.Model.UserModel;
import MicroUser.UserSpringBoot.Service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/user")
public class UserController {
    @Autowired
    private UserService userService;
    private static final Logger log = LoggerFactory.getLogger(UserController.class);


    @PostMapping("/create")
    public UserModel createUser(@RequestBody UserModel user) {
        log.info("POST /api/user/create Name : {}", user.getName());
        return userService.saveUser(user);
    }

    @GetMapping("/all")
    public List<UserModel> getAllUsers() {
        log.info("GET /api/user/all");
        return userService.getAllUsers();
    }

    @GetMapping("/get/{id}")
    public UserModel getUserById(@PathVariable Long id) {
        log.info("GET /api/user/get/{}", id);
        return userService.getUserById(id);
    }

    @PostMapping("/buy")
    public UserModel buyProduct(@RequestBody BuyRequestDto buyRequestDto) {
        log.info("POST /api/user/buy Product ID : {} User ID : {}", buyRequestDto.getProductId(), buyRequestDto.getUserId());
        return userService.buyProduct(buyRequestDto);
    }
}
