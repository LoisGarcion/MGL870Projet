package MicroUser.UserSpringBoot.Controller;

import MicroUser.UserSpringBoot.Model.K6Model;
import MicroUser.UserSpringBoot.Service.K6Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/k6")
public class K6Controller {
    private static final Logger log = LoggerFactory.getLogger(K6Controller.class);
    @Autowired
    private K6Service k6Service;

    @PostMapping("/createBlock")
    public K6Model createBlock (@RequestBody K6Model block) {
        log.info("Creating block {}", block.isAnomaly());
        return k6Service.saveK6Model(block);
    }

    @GetMapping("/all")
    public List<K6Model> getAllBlocks() {
        return k6Service.getAllBlocks();
    }
}
