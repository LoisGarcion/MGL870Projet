package MicroUser.UserSpringBoot.Controller;

import MicroUser.UserSpringBoot.Dto.BuyRequestDto;
import MicroUser.UserSpringBoot.Model.UserModel;
import MicroUser.UserSpringBoot.Service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/user")
public class UserController {
    @Autowired
    private UserService userService;

    @PostMapping("/create")
    public UserModel createUser(@RequestBody UserModel user) {
        return userService.saveUser(user);
    }

    @GetMapping("/all")
    public List<UserModel> getAllUsers() {
        return userService.getAllUsers();
    }

    @PostMapping("/buy")
    public UserModel buyProduct(@RequestBody BuyRequestDto buyRequestDto) {
        return userService.buyProduct(buyRequestDto);
    }
}
