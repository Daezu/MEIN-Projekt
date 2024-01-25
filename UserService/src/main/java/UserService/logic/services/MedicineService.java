package UserService.logic.services;

import UserService.logic.Entities.Medicine;
import UserService.logic.Entities.MedicineID;
import UserService.logic.Respositories.MedicineRepository;
import UserService.logic.ports.MedicinePort;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.BeanWrapper;
import org.springframework.beans.BeanWrapperImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataAccessException;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.HashSet;
import java.util.Optional;
import java.util.Set;

@Service
public class MedicineService implements MedicinePort {
    private final MedicineRepository medicineRepository;

    @Autowired
    public MedicineService(MedicineRepository medicineRepository) {
        this.medicineRepository = medicineRepository;
    }


    @Override
    public Medicine createMedicine(Long userId, String name, String dose, Long firstIntake, Long lastIntake) {
        Medicine u = new Medicine(Instant.now(), userId, name, dose, Instant.ofEpochSecond(firstIntake), Instant.ofEpochSecond(lastIntake));
        try {
            return medicineRepository.save(u);
        } catch (DataAccessException e) {
            e.printStackTrace();
            throw new RuntimeException("Unexpected error occurred");
        }
    }

    @Override
    public Optional<Medicine> getMedicine(MedicineID id) {
        if (id == null) {
            throw new RuntimeException();
        }
        return medicineRepository.findById(id);
    }

    @Override
    public Iterable<Medicine> findByUserId(Long userId) {
        return medicineRepository.findByUserid(userId);
    }

    @Override
    public Medicine patchMedicine(MedicineID id, Medicine patchedMedicine) {
        Medicine existingMedicine = medicineRepository.findById(id).orElse(null);
        if (existingMedicine != null) {
            BeanUtils.copyProperties(patchedMedicine, existingMedicine, getNullPropertyNames(patchedMedicine));
            return medicineRepository.save(existingMedicine);
        }
        return null;
    }

    @Override
    public boolean deleteMedicine(MedicineID id){
        if(medicineRepository.existsById(id)){
            medicineRepository.deleteById(id);
            return true;
        }
        return false;
    }

    private static String[] getNullPropertyNames(Object source) {
        final BeanWrapper src = new BeanWrapperImpl(source);
        java.beans.PropertyDescriptor[] pds = src.getPropertyDescriptors();

        Set<String> emptyNames = new HashSet<>();
        for (java.beans.PropertyDescriptor pd : pds) {
            Object srcValue = src.getPropertyValue(pd.getName());
            if (srcValue == null) {
                emptyNames.add(pd.getName());
            }
        }

        String[] result = new String[emptyNames.size()];
        return emptyNames.toArray(result);
    }

}
