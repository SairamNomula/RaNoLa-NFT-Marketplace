package com.ranola.marketplace.service;

import com.ranola.marketplace.dto.request.CreateNftRequest;
import com.ranola.marketplace.dto.response.NftResponse;
import com.ranola.marketplace.entity.Nft;
import com.ranola.marketplace.entity.User;
import com.ranola.marketplace.exception.BadRequestException;
import com.ranola.marketplace.exception.ResourceNotFoundException;
import com.ranola.marketplace.repository.NftRepository;
import com.ranola.marketplace.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
@RequiredArgsConstructor
public class NftService {

    private final NftRepository nftRepository;
    private final UserRepository userRepository;
    private final FileStorageService fileStorageService;

    public NftResponse createNft(CreateNftRequest request, MultipartFile image, String username) {
        User creator = userRepository.findByUsername(username)
                .orElseThrow(() -> new ResourceNotFoundException("User", "username", username));

        String imageFilename = fileStorageService.storeFile(image);

        Nft nft = Nft.builder()
                .name(request.getName())
                .description(request.getDescription())
                .imageUrl("/api/files/" + imageFilename)
                .price(request.getPrice())
                .royaltyPercentage(request.getRoyaltyPercentage())
                .category(request.getCategory())
                .creator(creator)
                .owner(creator)
                .status("LISTED")
                .build();

        nft = nftRepository.save(nft);
        return NftResponse.from(nft);
    }

    public Page<NftResponse> getNfts(int page, int size, String sort, String status, String search) {
        Sort sortOrder = "popular".equals(sort)
                ? Sort.by(Sort.Direction.DESC, "createdAt")
                : Sort.by(Sort.Direction.DESC, "createdAt");

        Pageable pageable = PageRequest.of(page, size, sortOrder);

        Page<Nft> nfts;
        if (search != null && !search.isBlank()) {
            nfts = nftRepository.findByNameContainingIgnoreCase(search, pageable);
        } else if (status != null && !status.isBlank()) {
            nfts = nftRepository.findByStatus(status, pageable);
        } else {
            nfts = nftRepository.findAll(pageable);
        }

        return nfts.map(NftResponse::from);
    }

    public NftResponse getNftById(Long id) {
        Nft nft = nftRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("NFT", "id", id));
        return NftResponse.from(nft);
    }

    public NftResponse updateNft(Long id, CreateNftRequest request, String username) {
        Nft nft = nftRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("NFT", "id", id));

        if (!nft.getCreator().getUsername().equals(username)) {
            throw new BadRequestException("You can only update your own NFTs");
        }

        if (request.getName() != null) nft.setName(request.getName());
        if (request.getDescription() != null) nft.setDescription(request.getDescription());
        if (request.getPrice() != null) nft.setPrice(request.getPrice());
        if (request.getRoyaltyPercentage() != null) nft.setRoyaltyPercentage(request.getRoyaltyPercentage());
        if (request.getCategory() != null) nft.setCategory(request.getCategory());

        nft = nftRepository.save(nft);
        return NftResponse.from(nft);
    }

    public void deleteNft(Long id, String username) {
        Nft nft = nftRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("NFT", "id", id));

        if (!nft.getCreator().getUsername().equals(username)) {
            throw new BadRequestException("You can only delete your own NFTs");
        }

        nftRepository.delete(nft);
    }
}
