package MicroUser.UserSpringBoot.Service;

import MicroUser.UserSpringBoot.Dto.BuyRequestDto;
import MicroUser.UserSpringBoot.Model.UserModel;
import MicroUser.UserSpringBoot.Repository.UserRepository;
import MicroUser.UserSpringBoot.ResponseModel.ProductResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.event.Level;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.Objects;

@Service
public class UserService {
    private RestTemplate restTemplate;
    private static final Logger log = LoggerFactory.getLogger(UserService.class);
    @Autowired
    private UserRepository userRepository;

    public UserModel saveUser(UserModel user) {
        log.info("Saving user");
        return userRepository.save(user);
    }

    public List<UserModel> getAllUsers() {
        log.info("Getting all users");
        return userRepository.findAll();
    }

    public UserModel buyProduct(BuyRequestDto buyRequestDto) {
        log.info("Buying product");
        restTemplate = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        headers.set("Content-Type", "application/json");

        // Create the request entity
        HttpEntity<String> request = new HttpEntity<>(headers);

        // Make the GET request
        ResponseEntity<ProductResponse> response = restTemplate.exchange("http://product-app:8080/api/product/get/" + buyRequestDto.getProductId(), HttpMethod.GET, request, ProductResponse.class);
        if (response.getStatusCode().is2xxSuccessful()) {
            log.info("Product found");
            UserModel user = userRepository.findById(buyRequestDto.getUserId()).orElse(null);
            if (user != null) {
                log.info("User found");
                user.setMoney(user.getMoney() - Objects.requireNonNull(response.getBody()).getProductPrice());
                return userRepository.save(user);
            } else {
                log.error("User not found");
                return null;
            }
        } else {
            log.error("Product not found");
            return null;
        }
    }
}
