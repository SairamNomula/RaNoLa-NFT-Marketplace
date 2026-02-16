package com.ranola.marketplace.repository;

import com.ranola.marketplace.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.domain.Pageable;

import java.util.List;
import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByUsername(String username);

    Optional<User> findByEmail(String email);

    Optional<User> findByWalletAddress(String walletAddress);

    boolean existsByUsername(String username);

    boolean existsByEmail(String email);

    @Query("SELECT DISTINCT a.seller FROM Auction a WHERE a.status = 'CLOSED' ORDER BY a.seller.id")
    List<User> findTopSellers(Pageable pageable);
}
