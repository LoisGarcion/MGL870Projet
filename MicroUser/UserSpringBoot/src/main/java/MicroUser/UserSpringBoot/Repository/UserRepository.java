package MicroUser.UserSpringBoot.Repository;

import MicroUser.UserSpringBoot.Model.UserModel;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<UserModel, Long> {
}
