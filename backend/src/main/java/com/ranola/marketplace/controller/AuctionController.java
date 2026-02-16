package com.ranola.marketplace.controller;

import com.ranola.marketplace.dto.request.CreateAuctionRequest;
import com.ranola.marketplace.dto.request.PlaceBidRequest;
import com.ranola.marketplace.dto.response.AuctionResponse;
import com.ranola.marketplace.dto.response.BidResponse;
import com.ranola.marketplace.service.AuctionService;
import com.ranola.marketplace.service.BidService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/auctions")
@RequiredArgsConstructor
public class AuctionController {

    private final AuctionService auctionService;
    private final BidService bidService;

    @PostMapping
    public ResponseEntity<AuctionResponse> createAuction(
            @Valid @RequestBody CreateAuctionRequest request,
            @AuthenticationPrincipal UserDetails userDetails) {
        AuctionResponse auction = auctionService.createAuction(request, userDetails.getUsername());
        return ResponseEntity.status(HttpStatus.CREATED).body(auction);
    }

    @GetMapping
    public ResponseEntity<Page<AuctionResponse>> getAuctions(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "12") int size,
            @RequestParam(required = false) String status) {
        return ResponseEntity.ok(auctionService.getAuctions(page, size, status));
    }

    @GetMapping("/{id}")
    public ResponseEntity<AuctionResponse> getAuctionById(@PathVariable Long id) {
        return ResponseEntity.ok(auctionService.getAuctionById(id));
    }

    @PutMapping("/{id}/close")
    public ResponseEntity<AuctionResponse> closeAuction(
            @PathVariable Long id,
            @AuthenticationPrincipal UserDetails userDetails) {
        return ResponseEntity.ok(auctionService.closeAuction(id, userDetails.getUsername()));
    }

    @PostMapping("/{auctionId}/bids")
    public ResponseEntity<BidResponse> placeBid(
            @PathVariable Long auctionId,
            @Valid @RequestBody PlaceBidRequest request,
            @AuthenticationPrincipal UserDetails userDetails) {
        BidResponse bid = bidService.placeBid(auctionId, request, userDetails.getUsername());
        return ResponseEntity.status(HttpStatus.CREATED).body(bid);
    }

    @GetMapping("/{auctionId}/bids")
    public ResponseEntity<List<BidResponse>> getBids(@PathVariable Long auctionId) {
        return ResponseEntity.ok(bidService.getBidsForAuction(auctionId));
    }
}
