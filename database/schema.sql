CREATE TABLE IF NOT EXISTS `orders` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
  `user_id` INTEGER,
  `order_type` TEXT NOT NULL CHECK(order_type IN ('boba', 'munchie', 'custom')),
  `shop` TEXT,
  `order_name` TEXT,
  `size` TEXT,
  `topping` TEXT,
  `description` TEXT,
  `status` TEXT CHECK(status IN ('ordered', 'delivering', 'delivered')) NOT NULL DEFAULT 'ordered',
  `rating` INTEGER CHECK(rating BETWEEN 1 AND 5),
  `created_at` TEXT DEFAULT CURRENT_TIMESTAMP,
  `delivered_at` TEXT DEFAULT NULL
);