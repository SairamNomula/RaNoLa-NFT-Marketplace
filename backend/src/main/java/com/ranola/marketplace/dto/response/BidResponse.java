package com.ranola.marketplace.dto.response;

import com.ranola.marketplace.entity.Bid;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@Builder
@AllArgsConstructor
public class BidResponse {

    private Long id;
    private Long auctionId;
    private UserResponse bidder;
    private BigDecimal amount;
    private LocalDateTime createdAt;

    public static BidResponse from(Bid bid) {
        return BidResponse.builder()
                .id(bid.getId())
                .auctionId(bid.getAuction().getId())
                .bidder(UserResponse.from(bid.getBidder()))
                .amount(bid.getAmount())
                .createdAt(bid.getCreatedAt())
                .build();
    }
}
