package UserService.logic.Respositories;

import UserService.logic.Entities.Medicine;
import UserService.logic.Entities.MedicineID;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;

public interface MedicineRepository extends CrudRepository<Medicine, MedicineID> {
    Iterable<Medicine> findByUserid(@Param("userid") Long userid);
}
