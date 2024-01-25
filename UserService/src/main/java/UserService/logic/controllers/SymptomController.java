package UserService.logic.controllers;

import UserService.logic.Entities.Symptom;
import UserService.logic.Entities.SymptomID;
import UserService.logic.ports.SymptomPort;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.time.Instant;
import java.util.Map;
import java.util.Optional;

@RestController
public class SymptomController {
    private final SymptomPort mySymptomPort;

    @Autowired
    public SymptomController(SymptomPort mySymptomPort) {
        this.mySymptomPort = mySymptomPort;
    }


    @GetMapping("/symptom")
    public Optional<Symptom> one(@RequestParam(name = "timestamp", defaultValue = "0") Long timestamp, @RequestParam(name = "userid", defaultValue = "0") Long userid) {
        return mySymptomPort.getSymptom(new SymptomID(Instant.ofEpochSecond(timestamp), userid));
    }

    @GetMapping("/symptom/search")
    public Iterable<Symptom> search(@RequestParam(name = "userid", defaultValue = "0") Long userid) {
        if(userid != 0)
            return mySymptomPort.findByUserId(userid);
        throw new RuntimeException();
    }

    @PostMapping("/symptom")
    public Symptom createSymptom(@RequestBody Map<String,String> body) {
        return mySymptomPort.createSymptom(Long.parseLong(body.get("userid")), body.get("name"), body.get("severity"), Long.parseLong(body.get("first_occurrence")), Long.parseLong(body.get("last_occurrence")));
    }

    @PatchMapping("/symptom/{id}")
    public Symptom patchSymptom(@PathVariable SymptomID id, @RequestBody Symptom patchedSymptom){
        return mySymptomPort.patchSymptom(id, patchedSymptom);
    }

    @DeleteMapping("/symptom/{id}")
    public boolean deleteSymptom(@PathVariable SymptomID id){
        return mySymptomPort.deleteSymptom(id);
    }

}
