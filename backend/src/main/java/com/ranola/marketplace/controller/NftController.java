package com.ranola.marketplace.controller;

import com.ranola.marketplace.dto.request.CreateNftRequest;
import com.ranola.marketplace.dto.response.NftResponse;
import com.ranola.marketplace.service.NftService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/nfts")
@RequiredArgsConstructor
public class NftController {

    private final NftService nftService;

    @PostMapping(consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<NftResponse> createNft(
            @Valid @RequestPart("nft") CreateNftRequest request,
            @RequestPart("image") MultipartFile image,
            @AuthenticationPrincipal UserDetails userDetails) {
        NftResponse nft = nftService.createNft(request, image, userDetails.getUsername());
        return ResponseEntity.status(HttpStatus.CREATED).body(nft);
    }

    @GetMapping
    public ResponseEntity<Page<NftResponse>> getNfts(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "12") int size,
            @RequestParam(required = false) String sort,
            @RequestParam(required = false) String status,
            @RequestParam(required = false) String search) {
        return ResponseEntity.ok(nftService.getNfts(page, size, sort, status, search));
    }

    @GetMapping("/{id}")
    public ResponseEntity<NftResponse> getNftById(@PathVariable Long id) {
        return ResponseEntity.ok(nftService.getNftById(id));
    }

    @PutMapping("/{id}")
    public ResponseEntity<NftResponse> updateNft(
            @PathVariable Long id,
            @Valid @RequestBody CreateNftRequest request,
            @AuthenticationPrincipal UserDetails userDetails) {
        return ResponseEntity.ok(nftService.updateNft(id, request, userDetails.getUsername()));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteNft(
            @PathVariable Long id,
            @AuthenticationPrincipal UserDetails userDetails) {
        nftService.deleteNft(id, userDetails.getUsername());
        return ResponseEntity.noContent().build();
    }
}
