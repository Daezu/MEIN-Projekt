package UserService.logic.Entities;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

//represents the user entity from the database
@Entity
@Table(name = "\"tbl_user\"")
@Getter
@Setter
public class User {
    @Id
    @SequenceGenerator(name = "user_id_seq", sequenceName = "user_id_seq")
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "user_id_seq")
    private Long userid;
    private String name;
    private String email;
    private String password;

    public User(){}

    public User(String name, String email, String password) {
        this.name = name;
        this.email = email;
        this.password = password;
    }
}
