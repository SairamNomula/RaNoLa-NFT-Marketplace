package com.ranola.marketplace.service;

import com.ranola.marketplace.dto.request.UpdateUserRequest;
import com.ranola.marketplace.dto.response.UserResponse;
import com.ranola.marketplace.entity.User;
import com.ranola.marketplace.exception.ResourceNotFoundException;
import com.ranola.marketplace.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;

    public UserResponse getUserById(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("User", "id", id));
        return UserResponse.from(user);
    }

    public UserResponse getUserByUsername(String username) {
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("User", "username", username));
        return UserResponse.from(user);
    }

    public UserResponse updateUser(Long id, UpdateUserRequest request) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("User", "id", id));

        if (request.getDisplayName() != null) user.setDisplayName(request.getDisplayName());
        if (request.getBio() != null) user.setBio(request.getBio());
        if (request.getWalletAddress() != null) user.setWalletAddress(request.getWalletAddress());
        if (request.getProfileImageUrl() != null) user.setProfileImageUrl(request.getProfileImageUrl());

        user = userRepository.save(user);
        return UserResponse.from(user);
    }

    public List<UserResponse> getTopSellers(int limit) {
        return userRepository.findTopSellers(PageRequest.of(0, limit))
                .stream()
                .map(UserResponse::from)
                .collect(Collectors.toList());
    }

    public List<UserResponse> getAllUsers() {
        return userRepository.findAll()
                .stream()
                .map(UserResponse::from)
                .collect(Collectors.toList());
    }
}
