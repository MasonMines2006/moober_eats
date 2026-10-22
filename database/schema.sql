CREATE TABLE IF NOT EXISTS `orders` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `order_type` TEXT NOT NULL CHECK(order_type IN ('premade', 'custom')),
  `shop` TEXT,
  `name` TEXT,
  `drink` TEXT,
  `size` TEXT,
  `topping` TEXT,
  `description` TEXT,
  `status` TEXT CHECK(status IN ('ordered', 'delivering', 'delivered')),
  `rating` INTEGER,
  `created_at` TEXT DEFAULT CURRENT_TIMESTAMP,
  `delivered_at` TEXT DEFAULT NULL
);