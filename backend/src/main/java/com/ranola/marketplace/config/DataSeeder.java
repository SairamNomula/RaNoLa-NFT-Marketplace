package com.ranola.marketplace.config;

import com.ranola.marketplace.entity.Auction;
import com.ranola.marketplace.entity.Nft;
import com.ranola.marketplace.entity.User;
import com.ranola.marketplace.repository.AuctionRepository;
import com.ranola.marketplace.repository.NftRepository;
import com.ranola.marketplace.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Component
@RequiredArgsConstructor
@Slf4j
public class DataSeeder implements CommandLineRunner {

    private final UserRepository userRepository;
    private final NftRepository nftRepository;
    private final AuctionRepository auctionRepository;
    private final PasswordEncoder passwordEncoder;

    @Override
    public void run(String... args) {
        if (userRepository.count() > 0) {
            log.info("Database already seeded, skipping...");
            return;
        }

        log.info("Seeding database with sample data...");

        // Create users
        User sairam = userRepository.save(User.builder()
                .username("sairam")
                .email("sairam@ranola.com")
                .passwordHash(passwordEncoder.encode("password123"))
                .displayName("Sairam Nomula")
                .bio("Creator of RaNoLa NFT Marketplace. Digital artist and developer.")
                .role("ADMIN")
                .build());

        User rudra = userRepository.save(User.builder()
                .username("rudra")
                .email("rudra@ranola.com")
                .passwordHash(passwordEncoder.encode("password123"))
                .displayName("Rudra")
                .bio("Digital artist specializing in illusion art.")
                .build());

        User david = userRepository.save(User.builder()
                .username("david")
                .email("david@ranola.com")
                .passwordHash(passwordEncoder.encode("password123"))
                .displayName("David")
                .bio("Robotic art enthusiast and NFT collector.")
                .build());

        User anonymous = userRepository.save(User.builder()
                .username("anonymous")
                .email("anon@ranola.com")
                .passwordHash(passwordEncoder.encode("password123"))
                .displayName("Anonymous")
                .bio("Mystery artist of the NFT world.")
                .build());

        // Create NFTs
        Nft illusions = nftRepository.save(Nft.builder()
                .name("Illusions")
                .description("A mesmerizing digital art piece exploring the boundaries of perception.")
                .imageUrl("/images/illusions.png")
                .price(new BigDecimal("1.7"))
                .royaltyPercentage(new BigDecimal("10"))
                .creator(rudra)
                .owner(rudra)
                .status("LISTED")
                .category("Digital Art")
                .build());

        Nft photography = nftRepository.save(Nft.builder()
                .name("Photography")
                .description("Stunning photography captured in the digital realm.")
                .imageUrl("/images/photography.png")
                .price(new BigDecimal("2.0"))
                .royaltyPercentage(new BigDecimal("5"))
                .creator(sairam)
                .owner(sairam)
                .status("LISTED")
                .category("Photography")
                .build());

        Nft roboticArts = nftRepository.save(Nft.builder()
                .name("Robotic Arts")
                .description("Where technology meets creativity - robotic-inspired digital art.")
                .imageUrl("/images/robotic-arts.png")
                .price(new BigDecimal("1.5"))
                .royaltyPercentage(new BigDecimal("8"))
                .creator(david)
                .owner(david)
                .status("LISTED")
                .category("Digital Art")
                .build());

        Nft arts = nftRepository.save(Nft.builder()
                .name("Arts")
                .description("A beautiful collection of abstract digital art.")
                .imageUrl("/images/arts.png")
                .price(new BigDecimal("1.0"))
                .royaltyPercentage(new BigDecimal("5"))
                .creator(anonymous)
                .owner(anonymous)
                .status("LISTED")
                .category("Abstract")
                .build());

        Nft splash = nftRepository.save(Nft.builder()
                .name("Splash")
                .description("Vibrant color splash art that brings energy to any collection.")
                .imageUrl("/images/splash.png")
                .price(new BigDecimal("0.8"))
                .royaltyPercentage(new BigDecimal("10"))
                .creator(sairam)
                .owner(sairam)
                .status("LISTED")
                .category("Abstract")
                .build());

        Nft fossill = nftRepository.save(Nft.builder()
                .name("Fossill")
                .description("Ancient meets digital in this fossil-inspired NFT artwork.")
                .imageUrl("/images/fossill.png")
                .price(new BigDecimal("1.2"))
                .royaltyPercentage(new BigDecimal("7"))
                .creator(rudra)
                .owner(rudra)
                .status("LISTED")
                .category("Digital Art")
                .build());

        Nft spiry = nftRepository.save(Nft.builder()
                .name("Spiry")
                .description("Spiral patterns that captivate the mind and soul.")
                .imageUrl("/images/spiry.png")
                .price(new BigDecimal("0.9"))
                .royaltyPercentage(new BigDecimal("5"))
                .creator(david)
                .owner(david)
                .status("LISTED")
                .category("Abstract")
                .build());

        Nft bleedArt = nftRepository.save(Nft.builder()
                .name("BleedArt")
                .description("Bold, bleeding color art that pushes creative boundaries.")
                .imageUrl("/images/bleedart.png")
                .price(new BigDecimal("1.5"))
                .royaltyPercentage(new BigDecimal("10"))
                .creator(anonymous)
                .owner(anonymous)
                .status("LISTED")
                .category("Digital Art")
                .build());

        // Create auctions
        LocalDateTime now = LocalDateTime.now();

        auctionRepository.save(Auction.builder()
                .nft(illusions)
                .seller(rudra)
                .startingPrice(new BigDecimal("1.7"))
                .currentPrice(new BigDecimal("1.7"))
                .currency("ETH")
                .startTime(now)
                .endTime(now.plusDays(7))
                .status("ACTIVE")
                .build());

        auctionRepository.save(Auction.builder()
                .nft(photography)
                .seller(sairam)
                .startingPrice(new BigDecimal("2.0"))
                .currentPrice(new BigDecimal("2.0"))
                .currency("ETH")
                .startTime(now)
                .endTime(now.plusDays(5))
                .status("ACTIVE")
                .build());

        auctionRepository.save(Auction.builder()
                .nft(roboticArts)
                .seller(david)
                .startingPrice(new BigDecimal("1.5"))
                .currentPrice(new BigDecimal("1.5"))
                .currency("ETH")
                .startTime(now)
                .endTime(now.plusDays(3))
                .status("ACTIVE")
                .build());

        auctionRepository.save(Auction.builder()
                .nft(arts)
                .seller(anonymous)
                .startingPrice(new BigDecimal("1.0"))
                .currentPrice(new BigDecimal("1.0"))
                .currency("ETH")
                .startTime(now)
                .endTime(now.plusDays(10))
                .status("ACTIVE")
                .build());

        log.info("Database seeded with 4 users, 8 NFTs, and 4 auctions.");
    }
}
