package UserService.logic.controllers;

import UserService.logic.Exceptions.DatabaseException;
import UserService.logic.Exceptions.DuplicateEmailException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

//Controller to catch Exception thrown in the REST controller
@ControllerAdvice
public class ExceptionController {

    //catches DuplicateEmailException
    @ExceptionHandler(DuplicateEmailException.class)
    public ResponseEntity<String> handleDuplicateEmailException(DuplicateEmailException ex) {
        // You can customize the HTTP status and response message based on your requirements
        return new ResponseEntity<>("Email already exists", HttpStatus.CONFLICT);
    }

    //catches DatabaseException
    @ExceptionHandler(DatabaseException.class)
    public ResponseEntity<String> handleDatabaseException(DatabaseException ex) {
        // You can customize the HTTP status and response message based on your requirements
        return new ResponseEntity<>("Database error occurred", HttpStatus.INTERNAL_SERVER_ERROR);
    }

    //catches MissingServletRequestParameterException
    @ExceptionHandler(MissingServletRequestParameterException.class)
    public ResponseEntity<String> handleDatabaseException(MissingServletRequestParameterException ex) {
        // You can customize the HTTP status and response message based on your requirements
        String errorMessage = "Missing parameter: " + ex.getParameterName();
        return new ResponseEntity<>(errorMessage, HttpStatus.BAD_REQUEST);
    }

    //catches all other Exceptions
    @ExceptionHandler(Exception.class)
    public ResponseEntity<String> handleUnexpectedException(Exception ex) {
        // You can customize the HTTP status and response message based on your requirements
        return new ResponseEntity<>("Unexpected error occurred", HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
