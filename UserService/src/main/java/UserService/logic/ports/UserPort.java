package UserService.logic.ports;

import UserService.logic.Entities.User;
import UserService.logic.Exceptions.DatabaseException;
import UserService.logic.Exceptions.DuplicateEmailException;

import java.util.Optional;

//port for user/user_service table
public interface UserPort {
    User createUser(String name, String email, String password) throws DuplicateEmailException, DatabaseException;
    Optional<User> getUser(Long userId);
    Iterable<User> getAllUsers();
    Iterable<User> findByEmail(String email);
    User patchUser(Long id, User patchedUser);
    boolean deleteUser(Long userId);
}
