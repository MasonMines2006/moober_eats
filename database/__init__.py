import aiosqlite


class DatabaseManager:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    async def create_order(
        self, user_id: int, shop: str = '-', order_name: str = '-', size: str = '-', topping: str = '-', description: str = '-', order_type: str = "-"
    ) -> int | None:
        """
        This function will create an order in the database.
        This function will create a menu order in the database.
        :param user_id: The ID of the user associated with the order.
        :param shop: The name of the shop.
        :param order_name: The name of the order.
        :param size: The size of the order.
        :param topping: The topping of the order.
        :param description: The description of the order.
        :param order_type: The type of the order (e.g., 'munchie' or 'custom').
        """
        cursor = await self.connection.execute(
            "INSERT INTO orders(user_id, shop, order_name, size, topping, description, created_at, order_type) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)",
            (
                user_id,
                shop,
                order_name,
                size,
                topping,
                description,
                order_type,
            ),
        )
        await self.connection.commit()
        return cursor.lastrowid

    async def get_order_by_id(
        self, id: int
    ) -> dict | None:
        """
        This function will retrieve an order by its ID from the database.

        :param id: The ID of the order in the database.
        """
        cursor = await self.connection.execute(
            "SELECT * FROM orders WHERE id = ?",
            (id,),
        )
        row = await cursor.fetchone()
        return dict(row) if row else None

    
        
    async def update_order_status(
        self, id: int, status: str
    ) -> int | None:
        """
        This function will update the status of a order in the database.

        :param id: The ID of the order in the database.
        :param status: The status value to be stored in the database.
        """
        cursor = await self.connection.execute(
            "UPDATE orders SET status = ? WHERE id = ?",
            (status, id),       
        )
        if status == 'delivered':
            await self.connection.execute(
                "UPDATE orders SET delivered_at = CURRENT_TIMESTAMP WHERE id = ?",
                (id,),
            )
        await self.connection.commit()
        return cursor.rowcount == 1   

    async def add_order_rating(
            self, id: int, rating: str
        ) -> int:
            """
            This function will update the rating of a order in the database.
    
            :param id: The ID of the order in the database.
            :param rating: The rating value to be stored in the database for the order.
            """
            cursor = await self.connection.execute(
                "UPDATE orders SET rating = ? WHERE id = ?",
                (rating, id),       
            )
            await self.connection.commit()
            return cursor.rowcount == 1  # Returns True if the rating was successfully updated, False otherwise.

    async def get_recent_orders(
                self, user_id: int, limit: int = 5
            ) -> list:
                """
                This function will retrieve recent orders for a user from the database.

                :param user_id: The ID of the user in the database.
                :param limit: The maximum number of orders to retrieve.
                """
                cursor = await self.connection.execute(
                    "SELECT * FROM orders WHERE user_id = ? ORDER BY id DESC LIMIT ?",
                    (user_id, limit),       
                )
                return list(await cursor.fetchall())
