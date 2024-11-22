package MicroUser.UserSpringBoot.Service;

import MicroUser.UserSpringBoot.Model.K6Model;
import MicroUser.UserSpringBoot.Repository.K6Repository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class K6Service {
    @Autowired
    private K6Repository k6Repository;

    public K6Model saveK6Model(K6Model block) {
        block.setTimestamp(System.currentTimeMillis());
        return k6Repository.save(block);
    }

    public List<K6Model> getAllBlocks() {
        return k6Repository.findAll();
    }
}
