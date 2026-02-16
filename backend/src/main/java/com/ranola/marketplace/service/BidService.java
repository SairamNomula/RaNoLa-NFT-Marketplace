package com.ranola.marketplace.service;

import com.ranola.marketplace.dto.request.PlaceBidRequest;
import com.ranola.marketplace.dto.response.BidResponse;
import com.ranola.marketplace.entity.Auction;
import com.ranola.marketplace.entity.Bid;
import com.ranola.marketplace.entity.User;
import com.ranola.marketplace.exception.BadRequestException;
import com.ranola.marketplace.exception.ResourceNotFoundException;
import com.ranola.marketplace.repository.AuctionRepository;
import com.ranola.marketplace.repository.BidRepository;
import com.ranola.marketplace.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class BidService {

    private final BidRepository bidRepository;
    private final AuctionRepository auctionRepository;
    private final UserRepository userRepository;

    @Transactional
    public BidResponse placeBid(Long auctionId, PlaceBidRequest request, String username) {
        Auction auction = auctionRepository.findById(auctionId)
                .orElseThrow(() -> new ResourceNotFoundException("Auction", "id", auctionId));

        if (!"ACTIVE".equals(auction.getStatus())) {
            throw new BadRequestException("This auction is no longer active");
        }

        User bidder = userRepository.findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("User", "username", username));

        if (auction.getSeller().getId().equals(bidder.getId())) {
            throw new BadRequestException("You cannot bid on your own auction");
        }

        if (request.getAmount().compareTo(auction.getCurrentPrice()) <= 0) {
            throw new BadRequestException("Bid must be higher than current price: " + auction.getCurrentPrice());
        }

        Bid bid = Bid.builder()
                .auction(auction)
                .bidder(bidder)
                .amount(request.getAmount())
                .build();

        bid = bidRepository.save(bid);

        auction.setCurrentPrice(request.getAmount());
        auctionRepository.save(auction);

        return BidResponse.from(bid);
    }

    public List<BidResponse> getBidsForAuction(Long auctionId) {
        return bidRepository.findByAuctionIdOrderByAmountDesc(auctionId)
                .stream()
                .map(BidResponse::from)
                .collect(Collectors.toList());
    }
}
