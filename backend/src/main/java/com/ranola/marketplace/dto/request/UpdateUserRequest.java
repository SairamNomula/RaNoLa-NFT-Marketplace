package com.ranola.marketplace.dto.request;

import lombok.Data;

@Data
public class UpdateUserRequest {

    private String displayName;
    private String bio;
    private String walletAddress;
    private String profileImageUrl;
}
