package UserService.logic.controllers;

import UserService.logic.Entities.Medicine;
import UserService.logic.Entities.MedicineID;
import UserService.logic.ports.MedicinePort;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.time.Instant;
import java.util.Map;
import java.util.Optional;

@RestController
public class MedicineController {
    private final MedicinePort myMedicinePort;

    @Autowired
    public MedicineController(MedicinePort myMedicinePort) {
        this.myMedicinePort = myMedicinePort;
    }


    @GetMapping("/medicine")
    public Optional<Medicine> one(@RequestParam(name = "timestamp", defaultValue = "0") Long timestamp, @RequestParam(name = "userid", defaultValue = "0") Long userid) {
        return myMedicinePort.getMedicine(new MedicineID(Instant.ofEpochSecond(timestamp), userid));
    }

    @GetMapping("/medicine/search")
    public Iterable<Medicine> search(@RequestParam(name = "userid", defaultValue = "0") Long userid) {
        if(userid != 0) return myMedicinePort.findByUserId(userid);
        throw new RuntimeException();
    }

    @PostMapping("/medicine")
    public Medicine createMedicine(@RequestBody Map<String,String> body) {
        return myMedicinePort.createMedicine(Long.parseLong(body.get("userid")), body.get("name"), body.get("dose"), Long.parseLong(body.get("first_intake")), Long.parseLong(body.get("last_intake")));
    }

    @PatchMapping("/medicine/{id}")
    public Medicine patchMedicine(@PathVariable MedicineID id, @RequestBody Medicine patchedSymptom){
        return myMedicinePort.patchMedicine(id, patchedSymptom);
    }

    @DeleteMapping("/medicine/{id}")
    public boolean deleteMedicine(@PathVariable MedicineID id){
        return myMedicinePort.deleteMedicine(id);
    }

}
