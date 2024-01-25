package UserService.logic.Respositories;

import UserService.logic.Entities.Symptom;
import UserService.logic.Entities.SymptomID;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;

public interface SymptomRepository extends CrudRepository<Symptom, SymptomID> {
    //Symptom createSymptom(String name, String severity, Long firstOccurrence, Long lastOccurrence);
    Iterable<Symptom> findByUserid(@Param("userid") Long userid);
    //Optional<Symptom> getSymptom(SymptomID id);
    //Symptom patchSymptom(SymptomID id, Symptom patchedSymptom);
    //boolean deleteSymptom(SymptomID id);
}
