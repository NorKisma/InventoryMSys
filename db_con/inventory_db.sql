-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 26, 2024 at 12:51 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */
;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */
;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */
;
/*!40101 SET NAMES utf8mb4 */
;
--
-- Database: `inventory_db`
--

-- --------------------------------------------------------
--
-- Table structure for table `company_settings`
--

CREATE TABLE `company_settings` (
  `id` int(11) NOT NULL,
  `company_name` varchar(255) NOT NULL,
  `shortName` varchar(50) NOT NULL,
  `logo` varchar(255) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `tel` varchar(20) DEFAULT NULL,
  `website` varchar(100) DEFAULT NULL,
  `Datet` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;
--
-- Dumping data for table `company_settings`
--

INSERT INTO `company_settings` (
    `id`,
    `company_name`,
    `shortName`,
    `logo`,
    `address`,
    `email`,
    `tel`,
    `website`,
    `Datet`
  )
VALUES (
    11,
    'Inventory Management System',
    'IMS',
    'static/uploads/logo.jpeg',
    'kismayo',
    'nor.jws@gmail.com',
    '610754637',
    'www.IMS.com',
    '2024-08-13 18:26:39'
  ),
  (
    12,
    'Inventory Management System',
    'IMS',
    'static/uploads/download.jpeg',
    'kismayo',
    'nor.jws@gmail.com',
    '610754637',
    'www.IMS.com',
    '2024-08-13 18:26:39'
  );
-- --------------------------------------------------------
--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `id` int(255) NOT NULL,
  `Customer_Name` varchar(200) NOT NULL,
  `tel` varchar(20) NOT NULL,
  `gender` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  `DateT` varchar(50) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;
--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (
    `id`,
    `Customer_Name`,
    `tel`,
    `gender`,
    `email`,
    `DateT`
  )
VALUES (
    1,
    'Nor Mohamed',
    '0617778899',
    'male',
    'Abdifitax@gmail.com',
    '2024-08-19'
  ),
  (
    3,
    ' Mohamed',
    '88888888',
    'male',
    'Abdifitaax@gmail.com',
    '2024-08-16'
  ),
  (
    4,
    ' Mohamed',
    '0617778899',
    'male',
    'Abdifitaax@gmail.com',
    '2024-07-31'
  ),
  (
    5,
    'Nor Mohamed',
    '66666666666',
    'male',
    'Abdifitaax@gmail.com',
    '2024-07-29'
  ),
  (
    11,
    'Hussein  Mohamed  ',
    '0617778899',
    'male',
    'nor.jws@gmail.com',
    '2024-08-21'
  ),
  (
    12,
    'BILL Boyad SADIIQ - CR / N/A',
    '0617778899',
    'male',
    'nor.jws@gmail.com',
    '2024-08-12'
  );
-- --------------------------------------------------------
--
-- Table structure for table `inventory`
--

CREATE TABLE `inventory` (
  `id` int(11) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `qty` int(11) NOT NULL,
  `type` tinyint(1) NOT NULL,
  `stock_from` enum('sales', 'receiving') NOT NULL,
  `form_id` int(11) NOT NULL,
  `date_updated` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;
-- --------------------------------------------------------
--
-- Table structure for table `product_list`
--

CREATE TABLE `product_list` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `product_unit` varchar(255) NOT NULL,
  `category_name` varchar(255) NOT NULL,
  `price` decimal(10, 2) NOT NULL,
  `description` text DEFAULT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;
--
-- Dumping data for table `product_list`
--

INSERT INTO `product_list` (
    `id`,
    `name`,
    `product_unit`,
    `category_name`,
    `price`,
    `description`
  )
VALUES (3, 'Baasto', 'PS', 'Electronic', 52.00, 'd'),
  (
    5,
    'Laptop',
    'PS',
    'Computers',
    52.00,
    'xcvcxvxc'
  );
-- --------------------------------------------------------
--
-- Table structure for table `purchase`
--

CREATE TABLE `purchase` (
  `order_id` int(11) NOT NULL,
  `invoice_number` varchar(100) DEFAULT NULL,
  `supp_id` int(11) NOT NULL,
  `product_id` int(20) NOT NULL,
  `product_unit` varchar(255) NOT NULL,
  `qty` int(11) NOT NULL,
  `price` decimal(10, 2) NOT NULL,
  `subtotal` decimal(10, 2) NOT NULL,
  `date_order` datetime NOT NULL,
  `date_updated` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `status` enum('Pending', 'Completed', 'Cancelled') NOT NULL DEFAULT 'Pending' FOREIGN KEY (supp_id) REFERENCES suppliers(id),
  FOREIGN KEY (product_id) REFERENCES products(id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;
-- --------------------------------------------------------
--
-- Table structure for table `suppliers`
--

CREATE TABLE `suppliers` (
  `supp_id` int(255) NOT NULL,
  `supp_name` varchar(200) NOT NULL,
  `supp_contact` varchar(200) NOT NULL,
  `supp_email` varchar(50) NOT NULL,
  `supp_company` varchar(200) NOT NULL,
  `supp_address` varchar(50) NOT NULL,
  `date_added` varchar(50) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;
--
-- Dumping data for table `suppliers`
--

INSERT INTO `suppliers` (
    `supp_id`,
    `supp_name`,
    `supp_contact`,
    `supp_email`,
    `supp_company`,
    `supp_address`,
    `date_added`
  )
VALUES (
    1,
    'nur mohamed hussein',
    '565464',
    'bbbb@gmail.com',
    'jubba',
    'kismayo',
    '2024-08-13'
  );
-- --------------------------------------------------------
--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `ful_name` varchar(200) NOT NULL,
  `tel` varchar(20) NOT NULL,
  `email` varchar(25) NOT NULL,
  `password` varchar(50) NOT NULL,
  `role` varchar(20) NOT NULL,
  `status` varchar(50) NOT NULL,
  `image` varchar(255) NOT NULL,
  `dateT` varchar(50) NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;
--
-- Dumping data for table `users`
--

INSERT INTO `users` (
    `id`,
    `ful_name`,
    `tel`,
    `email`,
    `password`,
    `role`,
    `status`,
    `image`,
    `dateT`
  )
VALUES (
    38,
    'Nor Mohamed ',
    '0617220603',
    'nor.jws@gmail.com',
    '7b7a53e239400a13bd6be6c91c4f6c4e',
    'admin',
    'Active',
    'nor.jpg',
    '2024-08-07'
  ),
  (
    47,
    'Mohamed Hussein ',
    '0617220622',
    'moha@gmail.com',
    '2d95666e2649fcfc6e3af75e09f5adb9',
    'admin',
    'Active',
    'NUUR.jpg',
    '2024-08-15'
  ),
  (
    48,
    'Mohamed Nor',
    '0617220304',
    'nor.jws@gmail.com',
    '2d95666e2649fcfc6e3af75e09f5adb9',
    'user',
    'Active',
    'Capture.PNG',
    '2024-08-14'
  ),
  (
    49,
    'Mohamed Hussein ',
    '0617220622',
    'moha@gmail.com',
    '2d95666e2649fcfc6e3af75e09f5adb9',
    'user',
    'Active',
    'nor_-_Copy.jpg',
    '2024-07-31'
  );
--
-- Indexes for dumped tables
--

--
-- Indexes for table `company_settings`
--
ALTER TABLE `company_settings`
ADD PRIMARY KEY (`id`);
--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
ADD PRIMARY KEY (`id`);
--
-- Indexes for table `inventory`
--
ALTER TABLE `inventory`
ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`),
  ADD KEY `product_id` (`product_id`);
--
-- Indexes for table `product_list`
--
ALTER TABLE `product_list`
ADD PRIMARY KEY (`id`);
--
-- Indexes for table `purchase`
--
ALTER TABLE `purchase`
ADD PRIMARY KEY (`order_id`);
--
-- Indexes for table `suppliers`
--
ALTER TABLE `suppliers`
ADD PRIMARY KEY (`supp_id`);
--
-- Indexes for table `users`
--
ALTER TABLE `users`
ADD PRIMARY KEY (`id`);
--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `company_settings`
--
ALTER TABLE `company_settings`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
  AUTO_INCREMENT = 13;
--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
MODIFY `id` int(255) NOT NULL AUTO_INCREMENT,
  AUTO_INCREMENT = 13;
--
-- AUTO_INCREMENT for table `inventory`
--
ALTER TABLE `inventory`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `product_list`
--
ALTER TABLE `product_list`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
  AUTO_INCREMENT = 6;
--
-- AUTO_INCREMENT for table `purchase`
--
ALTER TABLE `purchase`
MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT,
  AUTO_INCREMENT = 63;
--
-- AUTO_INCREMENT for table `suppliers`
--
ALTER TABLE `suppliers`
MODIFY `supp_id` int(255) NOT NULL AUTO_INCREMENT,
  AUTO_INCREMENT = 2;
--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
  AUTO_INCREMENT = 50;
COMMIT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */
;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */
;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */
;