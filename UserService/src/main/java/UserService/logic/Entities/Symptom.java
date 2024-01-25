package UserService.logic.Entities;


import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.Instant;

@Entity
@Table(name = "\"tbl_symptom\"")
@IdClass(SymptomID.class)
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Symptom {

    @Id
    @Temporal(TemporalType.TIMESTAMP)
    private Instant timestamp;
    @Id
    //@ManyToOne
    //@JoinColumn(name = "userid")
    //private User userid;
    private Long userid;
    @Column
    private String name;
    @Column
    private String severity;
    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "first_occurrence")
    private Instant first_occurrence;
    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "last_occurrence")
    private Instant last_occurrence;

    public Symptom(Long userid, String name, String severity, Instant first_occurrence, Instant last_occurrence) {
        this.userid = userid;
        this.name = name;
        this.severity = severity;
        this.first_occurrence = first_occurrence;
        this.last_occurrence = last_occurrence;
    }


}
