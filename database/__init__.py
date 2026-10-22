import aiosqlite


class DatabaseManager:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    async def create_drink(
        self, user_id: int, shop: str, drink: str, size: str, topping: str, description: str
    ) -> int | None:
        """
        This function will create an drink in the database.
        This function will create a menu drink in the database.
        :param user_id: The ID of the user associated with the drink.
        :param shop: The name of the shop.
        :param drink: The drink of the drink.
        :param size: The size of the drink.
        :param topping: The topping of the drink.
        :param description: The description of the drink.
        """
        cursor = await self.connection.execute(
            "INSERT INTO drinks(user_id, shop, drink, size, topping, description, created_at, drink_type) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, 'menu')",
            (
                user_id,
                shop,
                drink,
                size,
                topping,
                description,
            ),
        )
        await self.connection.commit()
        return cursor.lastrowid

    async def create_custom_drink(
        self, user_id: int, description: str
    ) -> int | None:
        """
        This function will create a custom drink in the database.

        :param user_id: The ID of the user associated with the custom drink.
        :param description: The description of the custom drink.
        :return: The ID of the newly created custom drink, or None if creation failed.
        """
        cursor = await self.connection.execute(
            "INSERT INTO drinks(user_id, description, created_at, drink_type) VALUES (?, ?, CURRENT_TIMESTAMP, 'custom')",
            (
                user_id,
                description,
            ),
        )
        await self.connection.commit()
        return cursor.lastrowid 
        
    async def update_status(
        self, id: int, status: str
    ) -> int | None:
        """
        This function will update the status of an drink in the database.

        :param id: The ID of the drink in the database.
        :param status: The status value to be stored in the database.
        """
        cursor = await self.connection.execute(
            "UPDATE drinks SET status = ? WHERE id = ?",
            (status, id),       
        )
        if status == 'delivered':
            await self.connection.execute(
                "UPDATE drinks SET delivered_at = CURRENT_TIMESTAMP WHERE id = ?",
                (id,),
            )
        await self.connection.commit()
        return cursor.rowcount == 1   

    async def add_rating(
            self, id: int, rating: str
        ) -> int:
            """
            This function will update the rating of an drink in the database.
    
            :param id: The ID of the drink in the database.
            :param rating: The rating value to be stored in the database for the drink.
            """
            cursor = await self.connection.execute(
                "UPDATE drinks SET rating = ? WHERE id = ?",
                (rating, id),       
            )
            await self.connection.commit()
            return cursor.rowcount == 1  # Returns True if the rating was successfully updated, False otherwise.

    async def get_recent_drinks(
                self, user_id: int, limit: int = 5
            ) -> list:
                """
                This function will retrieve recent drinks for a user from the database.
        
                :param user_id: The ID of the user in the database.
                :param limit: The maximum number of drinks to retrieve.
                """
                cursor = await self.connection.execute(
                    "SELECT * FROM drinks WHERE user_id = ? ORDER BY id DESC LIMIT ?",
                    (user_id, limit),       
                )
                return list(await cursor.fetchall())