package com.ranola.marketplace.repository;

import com.ranola.marketplace.entity.Nft;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface NftRepository extends JpaRepository<Nft, Long> {

    Page<Nft> findByStatus(String status, Pageable pageable);

    List<Nft> findByCreatorId(Long creatorId);

    List<Nft> findByOwnerId(Long ownerId);

    Page<Nft> findByCategory(String category, Pageable pageable);

    Page<Nft> findByNameContainingIgnoreCase(String name, Pageable pageable);
}
