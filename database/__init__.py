import aiosqlite


class DatabaseManager:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    async def create_order(
        self, user_id: int, shop: str, order_name: str, size: str, topping: str, description: str
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
        """
        cursor = await self.connection.execute(
            "INSERT INTO orders(user_id, shop, order_name, size, topping, description, created_at, order_type) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, 'menu')",
            (
                user_id,
                shop,
                order_name,
                size,
                topping,
                description,
            ),
        )
        await self.connection.commit()
        return cursor.lastrowid

    async def create_custom_order(
        self, user_id: int, description: str
    ) -> int | None:
        """
        This function will create a custom order in the database.

        :param user_id: The ID of the user associated with the custom order.
        :param description: The description of the custom order.
        :return: The ID of the newly created custom order, or None if creation failed.
        """
        cursor = await self.connection.execute(
            "INSERT INTO orders(user_id, description, created_at, order_type) VALUES (?, ?, CURRENT_TIMESTAMP, 'custom')",
            (
                user_id,
                description,
            ),
        )
        await self.connection.commit()
        return cursor.lastrowid 
        
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
