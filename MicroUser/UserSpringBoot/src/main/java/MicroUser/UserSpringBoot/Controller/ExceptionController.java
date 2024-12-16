package MicroUser.UserSpringBoot.Controller;

import MicroUser.UserSpringBoot.Model.UserModel;
import MicroUser.UserSpringBoot.Service.UserService;
import com.fasterxml.jackson.core.JsonParseException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.HttpRequestMethodNotSupportedException;
import org.springframework.web.bind.MissingServletRequestParameterException;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.ResourceAccessException;

import javax.naming.AuthenticationException;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.AccessDeniedException;
import java.sql.SQLException;
import java.util.ConcurrentModificationException;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.concurrent.TimeoutException;

@RestController
@RequestMapping("/api/exception")
public class ExceptionController {
    private static final Logger log = LoggerFactory.getLogger(ExceptionController.class);
    @GetMapping("/exception1")
    public String getException1() {
        log.info("GET /api/exception/exception1");
        throw new RuntimeException("This is a test runtime exception");
    }

    @GetMapping("/exception2")
    public String getException2() {
        log.info("GET /api/exception/exception2");
        throw new IllegalArgumentException("Invalid argument provided");
    }

    @GetMapping("/exception3")
    public String getException3() {
        log.info("GET /api/exception/exception3");
        throw new NullPointerException("Null value encountered");
    }

    @GetMapping("/exception4")
    public String getException4() {
        log.info("GET /api/exception/exception4");
        throw new IllegalStateException("Illegal state detected");
    }

    @GetMapping("/exception5")
    public String getException5() {
        log.info("GET /api/exception/exception5");
        throw new IndexOutOfBoundsException("Index out of bounds");
    }

    @GetMapping("/exception6")
    public String getException6() {
        log.info("GET /api/exception/exception6");
        throw new ArithmeticException("Arithmetic error, division by zero");
    }

    @GetMapping("/exception7")
    public String getException7() {
        log.info("GET /api/exception/exception7");
        throw new UnsupportedOperationException("Operation not supported");
    }

    @GetMapping("/exception8")
    public String getException8() {
        log.info("GET /api/exception/exception8");
        throw new NoSuchElementException("No such element found");
    }

    @GetMapping("/exception9")
    public String getException9() {
        log.info("GET /api/exception/exception9");
        throw new ClassCastException("Class cast exception occurred");
    }

    @GetMapping("/exception10")
    public String getException10() throws IOException {
        log.info("GET /api/exception/exception10");
        throw new IOException("I/O error occurred");
    }

    @GetMapping("/exception11")
    public String getException11() throws FileNotFoundException {
        log.info("GET /api/exception/exception11");
        throw new FileNotFoundException("File not found");
    }

    @GetMapping("/exception12")
    public String getException12() throws TimeoutException {
        log.info("GET /api/exception/exception12");
        throw new TimeoutException("Request timed out");
    }

    @GetMapping("/exception13")
    public String getException13() {
        log.info("GET /api/exception/exception13");
        throw new ConcurrentModificationException("Concurrent modification detected");
    }

    @GetMapping("/exception14")
    public String getException14() throws JsonParseException {
        log.info("GET /api/exception/exception14");
        throw new JsonParseException(null, "JSON parse error");
    }

    @GetMapping("/exception15")
    public String getException15() throws SQLException {
        log.info("GET /api/exception/exception15");
        throw new SQLException("SQL error occurred");
    }

    @GetMapping("/exception16")
    public String getException16() {
        log.info("GET /api/exception/exception16");
        throw new ResourceAccessException("Resource access denied");
    }

    @GetMapping("/exception17")
    public String getException17() throws AuthenticationException {
        log.info("GET /api/exception/exception17");
        throw new AuthenticationException("Authentication failed") {};
    }

    @GetMapping("/exception18")
    public String getException18() throws AccessDeniedException {
        log.info("GET /api/exception/exception18");
        throw new AccessDeniedException("Access denied");
    }

    @GetMapping("/exception19")
    public String getException19() throws HttpRequestMethodNotSupportedException {
        log.info("GET /api/exception/exception19");
        throw new HttpRequestMethodNotSupportedException("Method not supported");
    }

    @GetMapping("/exception20")
    public String getException20() throws MissingServletRequestParameterException {
        log.info("GET /api/exception/exception20");
        throw new MissingServletRequestParameterException("param", "String");
    }
}
