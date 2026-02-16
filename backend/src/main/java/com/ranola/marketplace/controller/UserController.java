package com.ranola.marketplace.controller;

import com.ranola.marketplace.dto.request.UpdateUserRequest;
import com.ranola.marketplace.dto.response.UserResponse;
import com.ranola.marketplace.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUserById(@PathVariable Long id) {
        return ResponseEntity.ok(userService.getUserById(id));
    }

    @PutMapping("/{id}")
    public ResponseEntity<UserResponse> updateUser(@PathVariable Long id,
                                                    @RequestBody UpdateUserRequest request) {
        return ResponseEntity.ok(userService.updateUser(id, request));
    }

    @GetMapping("/top-sellers")
    public ResponseEntity<List<UserResponse>> getTopSellers(
            @RequestParam(defaultValue = "10") int limit) {
        return ResponseEntity.ok(userService.getTopSellers(limit));
    }
}
