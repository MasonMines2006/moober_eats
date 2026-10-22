import aiosqlite


class DatabaseManager:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    async def create_order(
        self, shop: str, name: str, size: str, topping: str, description: str
    ) -> int | None:
        """
        This function will create an order in the database.

        :param shop: The name of the shop.
        :param name: The name of the order.
        :param size: The size of the order.
        :param topping: The topping of the order.
        :param description: The description of the order.
        """
        cursor = await self.connection.execute(
            "INSERT INTO orders(shop, name, size, topping, description, created_at) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
            (
                shop,
                name,
                size,
                topping,
                description,
            ),
        )
        await self.connection.commit()
        return cursor.lastrowid

    async def create_custom_order(
        self, id: int, description: str
    ) -> int | None:
        """
        This function will create a custom order in the database.

        :param id: The ID of the custom order.
        :param description: The description of the custom order.
        """
        cursor = await self.connection.execute(
            "INSERT INTO orders(id, description, created_at) VALUES (?, ?, CURRENT_TIMESTAMP)",
            (
                id,
                description,
            ),
        )
        await self.connection.commit()
        return cursor.lastrowid 
        
    async def update_status(
        self, id: int, status: str
    ) -> int | None:
        """
        This function will update the status of an order in the database.

        :param id: The ID of the order in the database.
        :param status: The status value to be stored in the database.
        """
        cursor = await self.connection.execute(
            "UPDATE orders SET status = ? WHERE id = ?",
            (status, id),       
        )
        await self.connection.commit()
        return cursor.rowcount == 1   

    async def add_rating(
            self, id: int, rating: str
        ) -> int:
            """
            This function will create a rating in the database.
    
            :param id: The ID of the rating in the database.
            :param rating: The rating value to be stored in the database.
            """
            cursor = await self.connection.execute(
                "UPDATE orders SET rating = ? WHERE id = ?",
                (rating, id),       
            )
            await self.connection.commit()
            return cursor.rowcount == 1  
            
    