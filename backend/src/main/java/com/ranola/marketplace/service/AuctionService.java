package com.ranola.marketplace.service;

import com.ranola.marketplace.dto.request.CreateAuctionRequest;
import com.ranola.marketplace.dto.response.AuctionResponse;
import com.ranola.marketplace.entity.Auction;
import com.ranola.marketplace.entity.Nft;
import com.ranola.marketplace.entity.User;
import com.ranola.marketplace.exception.BadRequestException;
import com.ranola.marketplace.exception.ResourceNotFoundException;
import com.ranola.marketplace.repository.AuctionRepository;
import com.ranola.marketplace.repository.NftRepository;
import com.ranola.marketplace.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
@RequiredArgsConstructor
public class AuctionService {

    private final AuctionRepository auctionRepository;
    private final NftRepository nftRepository;
    private final UserRepository userRepository;

    public AuctionResponse createAuction(CreateAuctionRequest request, String username) {
        User seller = userRepository.findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("User", "username", username));

        Nft nft = nftRepository.findById(request.getNftId())
                .orElseThrow(() -> new ResourceNotFoundException("NFT", "id", request.getNftId()));

        if (!nft.getOwner().getId().equals(seller.getId())) {
            throw new BadRequestException("You can only auction NFTs you own");
        }

        Auction auction = Auction.builder()
                .nft(nft)
                .seller(seller)
                .startingPrice(request.getStartingPrice())
                .currentPrice(request.getStartingPrice())
                .currency(request.getCurrency())
                .startTime(LocalDateTime.now())
                .endTime(request.getEndTime())
                .status("ACTIVE")
                .build();

        auction = auctionRepository.save(auction);
        return AuctionResponse.from(auction);
    }

    public Page<AuctionResponse> getAuctions(int page, int size, String status) {
        Pageable pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "createdAt"));

        Page<Auction> auctions;
        if (status != null && !status.isBlank()) {
            auctions = auctionRepository.findByStatus(status.toUpperCase(), pageable);
        } else {
            auctions = auctionRepository.findAll(pageable);
        }

        return auctions.map(AuctionResponse::from);
    }

    public AuctionResponse getAuctionById(Long id) {
        Auction auction = auctionRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Auction", "id", id));
        return AuctionResponse.from(auction);
    }

    public AuctionResponse closeAuction(Long id, String username) {
        Auction auction = auctionRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Auction", "id", id));

        if (!auction.getSeller().getUsername().equals(username)) {
            throw new BadRequestException("Only the seller can close this auction");
        }

        auction.setStatus("CLOSED");
        auction = auctionRepository.save(auction);
        return AuctionResponse.from(auction);
    }
}
