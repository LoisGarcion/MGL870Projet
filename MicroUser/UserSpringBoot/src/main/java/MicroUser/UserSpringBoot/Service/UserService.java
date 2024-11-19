package MicroUser.UserSpringBoot.Service;

import MicroUser.UserSpringBoot.Model.UserModel;
import MicroUser.UserSpringBoot.Repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.security.SecurityProperties;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;

    public UserModel saveUser(UserModel user) {
        return userRepository.save(user);
    }

    public List<UserModel> getAllUsers() {
        return userRepository.findAll();
    }
}
