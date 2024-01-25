package UserService.logic.ports;

import UserService.logic.Entities.Medicine;
import UserService.logic.Entities.MedicineID;

import java.util.Optional;

public interface MedicinePort {
    Medicine createMedicine(Long user, String name, String dose, Long firstIntake, Long lastIntake);
    Optional<Medicine> getMedicine(MedicineID id);
    Iterable<Medicine> findByUserId(Long userId);
    Medicine patchMedicine(MedicineID id, Medicine patchedMedicine);
    boolean deleteMedicine(MedicineID id);
}
