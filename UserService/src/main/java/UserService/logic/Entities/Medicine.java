package UserService.logic.Entities;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.Instant;

@Entity
@Table(name = "\"tbl_medicine\"")
@IdClass(MedicineID.class)
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Medicine {

    @Id
    //@CreationTimestamp
    @Temporal(TemporalType.TIMESTAMP)
    //@Column(updatable = false)
    private Instant timestamp;
    @Id
    //@ManyToOne
    //@JoinColumn(name = "userid")
    //private User userid;
    private Long userid;
    @Column
    private String name;
    @Column
    private String dose;
    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "first_intake")
    private Instant first_intake;
    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "last_intake")
    private Instant last_intake;

    /*
    @PrePersist
    protected void onCreate() {
        if (timestamp == null) {
            timestamp = Instant.now();
        }
    }
    */

    public Medicine(Long userid, String name, String dose, Instant first_intake, Instant last_intake) {
        this.userid = userid;
        this.name = name;
        this.dose = dose;
        this.first_intake = first_intake;
        this.last_intake = last_intake;
    }


}
