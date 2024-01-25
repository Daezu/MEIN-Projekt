package UserService.logic.Entities;

import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.time.Instant;
import java.util.Objects;

@AllArgsConstructor
@NoArgsConstructor
public class SymptomID  implements Serializable {
    private Instant timestamp;
    private Long userid;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof SymptomID that)) return false;
        return Objects.equals(timestamp, that.timestamp) && Objects.equals(userid, that.userid);
    }

    @Override
    public int hashCode() {
        return Objects.hash(timestamp, userid);
    }


}
