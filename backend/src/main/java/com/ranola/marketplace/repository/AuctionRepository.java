package com.ranola.marketplace.repository;

import com.ranola.marketplace.entity.Auction;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface AuctionRepository extends JpaRepository<Auction, Long> {

    Page<Auction> findByStatus(String status, Pageable pageable);

    List<Auction> findBySellerId(Long sellerId);

    List<Auction> findByNftId(Long nftId);
}
