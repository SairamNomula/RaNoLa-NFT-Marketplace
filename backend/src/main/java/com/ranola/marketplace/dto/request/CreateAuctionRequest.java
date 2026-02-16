package com.ranola.marketplace.dto.request;

import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
public class CreateAuctionRequest {

    @NotNull(message = "NFT ID is required")
    private Long nftId;

    @NotNull(message = "Starting price is required")
    @Positive(message = "Starting price must be positive")
    private BigDecimal startingPrice;

    private String currency = "ETH";

    @NotNull(message = "End time is required")
    private LocalDateTime endTime;
}
