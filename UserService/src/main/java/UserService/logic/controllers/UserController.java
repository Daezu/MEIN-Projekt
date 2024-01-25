package UserService.logic.controllers;

import UserService.logic.Entities.User;
import UserService.logic.Exceptions.DatabaseException;
import UserService.logic.Exceptions.DuplicateEmailException;
import UserService.logic.ports.UserPort;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.bind.annotation.*;

import java.util.Map;
import java.util.Optional;

//REST controller to save and get user/user_session entity
@RestController
public class UserController {
    private final UserPort myUserPort;

    @Autowired
    public UserController(UserPort myUserPort) {
        this.myUserPort = myUserPort;
    }

    //////////////////////////////
    //REST calls for user entity//
    //////////////////////////////

    //get all user from database
    @GetMapping("/user")
    public Iterable<User> all(){
        return myUserPort.getAllUsers();
    }

    //get one user by user id
    @GetMapping("/user/{id}")
    public Optional<User> one(@PathVariable Long id) {
        return myUserPort.getUser(id);
    }

    //search users by email address
    @GetMapping("/user/search")
    public Iterable<User> search(
            @RequestParam(name = "email", defaultValue = "") String email) throws MissingServletRequestParameterException {
        if(!email.isEmpty())
            return myUserPort.findByEmail(email);
        throw new MissingServletRequestParameterException("email", "String");
    }

    //create user by JSON in body with name, email and password
    @PostMapping("/user")
    public User createUser(@RequestBody Map<String,String> body) throws DuplicateEmailException, DatabaseException {
        return myUserPort.createUser(body.get("name"), body.get("email"), body.get("password"));
    }

    //patch user by id
    @PatchMapping("user/{id}")
    public User patchUser(@PathVariable Long id, @RequestBody User patchedUser){
        return myUserPort.patchUser(id, patchedUser);
    }

    //delete user by id
    @DeleteMapping("/user/{id}")
    public boolean deleteUser(@PathVariable Long id){
        return myUserPort.deleteUser(id);
    }

}
