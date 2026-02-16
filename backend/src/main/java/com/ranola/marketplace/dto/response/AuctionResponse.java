package com.ranola.marketplace.dto.response;

import com.ranola.marketplace.entity.Auction;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@Builder
@AllArgsConstructor
public class AuctionResponse {

    private Long id;
    private NftResponse nft;
    private UserResponse seller;
    private BigDecimal startingPrice;
    private BigDecimal currentPrice;
    private String currency;
    private LocalDateTime startTime;
    private LocalDateTime endTime;
    private String status;
    private LocalDateTime createdAt;

    public static AuctionResponse from(Auction auction) {
        return AuctionResponse.builder()
                .id(auction.getId())
                .nft(NftResponse.from(auction.getNft()))
                .seller(UserResponse.from(auction.getSeller()))
                .startingPrice(auction.getStartingPrice())
                .currentPrice(auction.getCurrentPrice())
                .currency(auction.getCurrency())
                .startTime(auction.getStartTime())
                .endTime(auction.getEndTime())
                .status(auction.getStatus())
                .createdAt(auction.getCreatedAt())
                .build();
    }
}
