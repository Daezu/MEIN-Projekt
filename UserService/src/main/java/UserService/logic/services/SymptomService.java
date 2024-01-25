package UserService.logic.services;

import UserService.logic.Entities.Symptom;
import UserService.logic.Entities.SymptomID;
import UserService.logic.Respositories.SymptomRepository;
import UserService.logic.ports.SymptomPort;
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
public class SymptomService implements SymptomPort {
    private final SymptomRepository symptomRepository;

    @Autowired
    public SymptomService(SymptomRepository symptomRepository) {
        this.symptomRepository = symptomRepository;
    }


    @Override
    public Symptom createSymptom(Long userId, String name, String severity, Long firstOccurrence, Long lastOccurrence) {
        Symptom u = new Symptom(Instant.now(), userId, name, severity, Instant.ofEpochSecond(firstOccurrence), Instant.ofEpochSecond(lastOccurrence));
        try {
            return symptomRepository.save(u);
        } catch (DataAccessException e) {
            throw new RuntimeException("Unexpected error occurred");
        }
    }

    @Override
    public Optional<Symptom> getSymptom(SymptomID id) {
        if (id == null) {
            throw new RuntimeException();
        }
        return symptomRepository.findById(id);
    }

    @Override
    public Iterable<Symptom> findByUserId(Long userId) {
        return symptomRepository.findByUserid(userId);
    }

    @Override
    public Symptom patchSymptom(SymptomID id, Symptom patchedSymptom) {
        Symptom existingSymptom = symptomRepository.findById(id).orElse(null);
        if (existingSymptom != null) {
            BeanUtils.copyProperties(patchedSymptom, existingSymptom, getNullPropertyNames(patchedSymptom));
            return symptomRepository.save(existingSymptom);
        }
        return null;
    }

    @Override
    public boolean deleteSymptom(SymptomID id){
        if(symptomRepository.existsById(id)){
            symptomRepository.deleteById(id);
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
