CREATE TABLE IF NOT EXISTS `warns` (
  `id` int(11) NOT NULL,
  `shop` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `size` varchar(20) NOT NULL,
  `topping` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `images` VARBINARY(MAX) NOT NULL,
  `rating` varchar(255) NOT NULL,
  `duration` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);