package com.ranola.marketplace.dto.response;

import com.ranola.marketplace.entity.Nft;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@Builder
@AllArgsConstructor
public class NftResponse {

    private Long id;
    private String name;
    private String description;
    private String imageUrl;
    private BigDecimal price;
    private BigDecimal royaltyPercentage;
    private String status;
    private String category;
    private UserResponse creator;
    private UserResponse owner;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    public static NftResponse from(Nft nft) {
        return NftResponse.builder()
                .id(nft.getId())
                .name(nft.getName())
                .description(nft.getDescription())
                .imageUrl(nft.getImageUrl())
                .price(nft.getPrice())
                .royaltyPercentage(nft.getRoyaltyPercentage())
                .status(nft.getStatus())
                .category(nft.getCategory())
                .creator(UserResponse.from(nft.getCreator()))
                .owner(UserResponse.from(nft.getOwner()))
                .createdAt(nft.getCreatedAt())
                .updatedAt(nft.getUpdatedAt())
                .build();
    }
}
