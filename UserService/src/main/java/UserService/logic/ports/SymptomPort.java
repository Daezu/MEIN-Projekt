package UserService.logic.ports;

import UserService.logic.Entities.Symptom;
import UserService.logic.Entities.SymptomID;

import java.util.Optional;

public interface SymptomPort {
    Symptom createSymptom(Long userId, String name, String severity, Long firstOccurrence, Long lastOccurrence);
    Optional<Symptom> getSymptom(SymptomID id);
    Iterable<Symptom> findByUserId(Long userId);
    Symptom patchSymptom(SymptomID id, Symptom patchedSymptom);
    boolean deleteSymptom(SymptomID id);
}
