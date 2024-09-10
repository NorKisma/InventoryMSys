-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 11, 2024 at 01:14 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `company_settings`
--

INSERT INTO `company_settings` (`id`, `company_name`, `shortName`, `logo`, `address`, `email`, `tel`, `website`, `Datet`) VALUES
(11, 'Inventory Management System', 'IMS', 'static/uploads/logo.jpeg', 'kismayo', 'nor.jws@gmail.com', '610754637', 'www.IMS.com', '2024-08-13 18:26:39'),
(12, 'Inventory Management System', 'IMS', 'static/uploads/download.jpeg', 'kismayo', 'nor.jws@gmail.com', '610754637', 'www.IMS.com', '2024-08-13 18:26:39');

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`id`, `Customer_Name`, `tel`, `gender`, `email`, `DateT`) VALUES
(1, 'Nor Mohamed', '0617778899', 'male', 'Abdifitax@gmail.com', '2024-08-19'),
(3, ' Mohamed', '88888888', 'male', 'Abdifitaax@gmail.com', '2024-08-16'),
(4, ' Mohamed', '0617778899', 'male', 'Abdifitaax@gmail.com', '2024-07-31'),
(5, 'Nor Mohamed', '66666666666', 'male', 'Abdifitaax@gmail.com', '2024-07-29'),
(11, 'Hussein  Mohamed  ', '0617778899', 'male', 'nor.jws@gmail.com', '2024-08-21');

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

CREATE TABLE `inventory` (
  `inventory_id` int(11) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `qty` int(255) NOT NULL,
  `stock_from` enum('sales','receiving') NOT NULL,
  `form_id` int(11) NOT NULL,
  `date_updated` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventory`
--

INSERT INTO `inventory` (`inventory_id`, `product_id`, `qty`, `stock_from`, `form_id`, `date_updated`) VALUES
(1, 5, 43, '', 0, '2024-09-10 16:09:21'),
(2, 6, 22, '', 0, '2024-09-10 16:13:25');

-- --------------------------------------------------------

--
-- Table structure for table `product_list`
--

CREATE TABLE `product_list` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `product_unit` varchar(255) NOT NULL,
  `category_name` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product_list`
--

INSERT INTO `product_list` (`id`, `name`, `product_unit`, `category_name`, `price`, `description`) VALUES
(5, 'Laptop', 'PS', 'Computers', 52.00, 'xcvcxvxc'),
(6, 'Desktop', 'PS', 'Computers', 52.00, 'Desktop  only one');

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
  `qty` int(50) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `date_order` datetime NOT NULL,
  `date_updated` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `status` enum('Pending','Received','Cancelled') NOT NULL DEFAULT 'Pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `purchase`
--

INSERT INTO `purchase` (`order_id`, `invoice_number`, `supp_id`, `product_id`, `product_unit`, `qty`, `price`, `subtotal`, `date_order`, `date_updated`, `status`) VALUES
(77, '13', 1, 3, 'PS', 88, 2.00, 176.00, '2024-08-09 00:00:00', '2024-08-26 14:05:44', 'Pending'),
(83, '12', 1, 5, 'PS', 6, 320.00, 1920.00, '2024-08-06 00:00:00', '2024-09-10 15:36:35', 'Received'),
(84, '1', 1, 6, 'PS', 22, 300.00, 6600.00, '2024-09-10 00:00:00', '2024-09-10 16:13:25', 'Received'),
(85, '2', 1, 5, 'PS', 30, 310.00, 9300.00, '2024-09-10 00:00:00', '2024-09-10 15:36:27', 'Received'),
(86, '3', 1, 5, 'PS', 15, 230.00, 3450.00, '2024-09-10 00:00:00', '2024-09-10 16:09:21', 'Received');

-- --------------------------------------------------------

--
-- Table structure for table `sales`
--

CREATE TABLE `sales` (
  `sale_id` int(11) NOT NULL,
  `cust_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `qty` int(11) NOT NULL,
  `price_sale` decimal(10,2) NOT NULL,
  `discount` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `payment` decimal(10,2) NOT NULL,
  `Balance` decimal(10,2) NOT NULL,
  `date_sale` date NOT NULL,
  `date_updated` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sales`
--

INSERT INTO `sales` (`sale_id`, `cust_id`, `product_id`, `qty`, `price_sale`, `discount`, `subtotal`, `payment`, `Balance`, `date_sale`, `date_updated`) VALUES
(1, 1, 5, 3, 52.00, 0.00, 156.00, 156.00, 0.00, '2024-09-10', '2024-09-10 22:38:34'),
(2, 1, 5, 1, 52.00, 0.00, 52.00, 0.00, 52.00, '2024-09-10', '2024-09-10 23:07:40');

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `suppliers`
--

INSERT INTO `suppliers` (`supp_id`, `supp_name`, `supp_contact`, `supp_email`, `supp_company`, `supp_address`, `date_added`) VALUES
(1, 'nur mohamed hussein', '565464', 'bbbb@gmail.com', 'jubba', 'kismayo', '2024-08-13');

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `ful_name`, `tel`, `email`, `password`, `role`, `status`, `image`, `dateT`) VALUES
(38, 'Nor Mohamed ', '0617220603', 'nor.jws@gmail.com', '7b7a53e239400a13bd6be6c91c4f6c4e', 'admin', 'Active', 'nor.jpg', '2024-08-07'),
(47, 'Mohamed Hussein ', '0617220622', 'moha@gmail.com', '2d95666e2649fcfc6e3af75e09f5adb9', 'admin', 'Active', 'NUUR.jpg', '2024-08-15'),
(48, 'Mohamed Nor', '0617220304', 'nor.jws@gmail.com', '2d95666e2649fcfc6e3af75e09f5adb9', 'user', 'Active', 'Capture.PNG', '2024-08-14'),
(49, 'Mohamed Hussein ', '0617220622', 'moha@gmail.com', '2d95666e2649fcfc6e3af75e09f5adb9', 'user', 'Active', 'nor_-_Copy.jpg', '2024-07-31');

-- --------------------------------------------------------

--
-- Stand-in structure for view `veiwcustomer`
-- (See below for the actual view)
--
CREATE TABLE `veiwcustomer` (
`Sale ID` int(11)
,`Sale Date` date
,`Customer ID` int(11)
,`Customer Name` varchar(200)
,`Telephone` varchar(20)
,`Product Name` varchar(255)
,`Quantity` int(11)
,`Price Sale` decimal(10,2)
,`Subtotal` decimal(10,2)
,`Paid Payment` decimal(10,2)
,`Balance` decimal(10,2)
);

-- --------------------------------------------------------

--
-- Structure for view `veiwcustomer`
--
DROP TABLE IF EXISTS `veiwcustomer`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `veiwcustomer`  AS SELECT `s`.`sale_id` AS `Sale ID`, `s`.`date_sale` AS `Sale Date`, `s`.`cust_id` AS `Customer ID`, `c`.`Customer_Name` AS `Customer Name`, `c`.`tel` AS `Telephone`, `p`.`name` AS `Product Name`, `s`.`qty` AS `Quantity`, `s`.`price_sale` AS `Price Sale`, `s`.`subtotal` AS `Subtotal`, `s`.`payment` AS `Paid Payment`, `s`.`Balance` AS `Balance` FROM ((`sales` `s` join `customers` `c` on(`s`.`cust_id` = `c`.`id`)) join `product_list` `p` on(`s`.`product_id` = `p`.`id`)) ;

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
  ADD PRIMARY KEY (`inventory_id`),
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
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `supp_id` (`supp_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `sales`
--
ALTER TABLE `sales`
  ADD PRIMARY KEY (`sale_id`),
  ADD KEY `cust_id` (`cust_id`),
  ADD KEY `product_id` (`product_id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `inventory`
--
ALTER TABLE `inventory`
  MODIFY `inventory_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `product_list`
--
ALTER TABLE `product_list`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `purchase`
--
ALTER TABLE `purchase`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=87;

--
-- AUTO_INCREMENT for table `sales`
--
ALTER TABLE `sales`
  MODIFY `sale_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `suppliers`
--
ALTER TABLE `suppliers`
  MODIFY `supp_id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=50;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `sales`
--
ALTER TABLE `sales`
  ADD CONSTRAINT `sales_ibfk_1` FOREIGN KEY (`cust_id`) REFERENCES `customers` (`id`),
  ADD CONSTRAINT `sales_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product_list` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
