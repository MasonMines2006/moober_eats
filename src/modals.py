import os
import random
import traceback

import discord

from src.client import MyClient
from src.links import (
    delivering_gifs,
    jinshi_fail_gifs,
    jinshi_success,
    maomao_gifs,
    maomao_success,
    restaurant_links,
)
from src.secret_imports import (
    CHANNEL_ID,
    MASON_DISCORD_ID,
)

HERE = os.path.dirname(__file__)
schema_path = os.path.join(HERE, "../database", "schema.sql")


class OtherInputModal(discord.ui.Modal, title="Specify Other Option"):
    # The text input component that receives freeform user text
    custom_choice = discord.ui.TextInput(
        label="Please specify:",
        placeholder="Type your custom option here...",
        max_length=100,
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Access the user's custom input via self.custom_choice.value
        user_text = self.custom_choice.value
        await interaction.response.send_message(
            f"You selected 'Other' and specified: **{user_text}**", ephemeral=True
        )


class BobaOrderModal(discord.ui.Modal, title="Boba Order"):
    shop = discord.ui.Label(
        text="Boba Shop Location",
        description="Select yummiest boba place",
        component=discord.ui.Select(
            placeholder="Where is Mason going to get boba?",
            required=False,
            options=[
                discord.SelectOption(label="Tea Hill CH"),
                discord.SelectOption(label="Moge Tea CH"),
                discord.SelectOption(label="Bobo Baba Cary"),
                discord.SelectOption(label="Moge Tea Raleigh"),
                discord.SelectOption(label="Other"),
            ],
        ),
    )
    boba_type = discord.ui.Label(
        text="Boba Type",
        description="Select the type of boba you want",
        component=discord.ui.Select(
            placeholder="what boba type are u getting?",
            required=False,
            options=[
                discord.SelectOption(label="Passion Fruit Green Tea"),
                discord.SelectOption(label="Yuzu Oolong"),
                discord.SelectOption(label="Superfruit Green Tea"),
                discord.SelectOption(label="Lemon Tea"),
                discord.SelectOption(label="Other"),
            ],
        ),
    )
    toppings = discord.ui.Label(
        text="Toppings",
        description="Select the toppings you want on your boba",
        component=discord.ui.Select(
            placeholder="What toppings do you want on your boba?",
            required=False,
            options=[
                discord.SelectOption(label="Normal Boba"),
                discord.SelectOption(label="Golden Bubble"),
                discord.SelectOption(label="None"),
            ],
        ),
    )
    size = discord.ui.Label(
        text="Size",
        description="Select the size of your boba",
        component=discord.ui.Select(
            placeholder="What size do you want your boba?",
            required=False,
            options=[
                discord.SelectOption(label="Large"),
                discord.SelectOption(label="Medium"),
                discord.SelectOption(label="Small"),
            ],
        ),
    )
    notes = discord.ui.Label(
        text="Notes",
        description="Other notes/custom orders",
        component=discord.ui.TextInput(
            style=discord.TextStyle.paragraph,
            placeholder="Add notes or details here for ur order.",
            max_length=2000,
            required=False,
        ),
    )

    async def select_callback(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
        if select.values[0] == "other":
            # Send the popup modal directly to the user who clicked "Other"
            await interaction.response.send_modal(OtherInputModal())
        else:
            # Handle regular static options normally
            await interaction.response.send_message(
                f"You selected: **{select.values[0]}**", ephemeral=True
            )

    def to_view(self, interaction: discord.Interaction) -> discord.ui.LayoutView:
        # Tell the type checker what our components are...
        assert isinstance(self.shop.component, discord.ui.Select)
        assert isinstance(self.boba_type.component, discord.ui.Select)
        assert isinstance(self.toppings.component, discord.ui.Select)
        assert isinstance(self.size.component, discord.ui.Select)
        assert isinstance(self.notes.component, discord.ui.TextInput)

        shop = self.shop.component.values[0] if self.shop.component.values else "-"
        boba_type = (
            self.boba_type.component.values[0]
            if self.boba_type.component.values
            else "-"
        )
        toppings = (
            self.toppings.component.values[0] if self.toppings.component.values else "-"
        )
        size = self.size.component.values[0] if self.size.component.values else "-"
        notes = self.notes.component.value if self.notes.component.value else "-"

        view = discord.ui.LayoutView()
        container = discord.ui.Container()
        view.add_item(container)

        container.add_item(discord.ui.TextDisplay("-# New Boba Order"))

        if shop:
            container.add_item(discord.ui.TextDisplay(f"Shop: {shop}"))
        if boba_type:
            container.add_item(discord.ui.TextDisplay(f"### Boba Type: {boba_type}"))
        if toppings:
            container.add_item(discord.ui.TextDisplay(f"### Toppings: {toppings}"))
        if size:
            container.add_item(discord.ui.TextDisplay(f"### Size: {size}"))
        if notes:
            container.add_item(discord.ui.TextDisplay(f"### Notes: {notes}"))

        return view

    async def on_submit(self, interaction: discord.Interaction):
        view = self.to_view(interaction)

        assert isinstance(self.shop.component, discord.ui.Select)
        assert isinstance(self.boba_type.component, discord.ui.Select)
        assert isinstance(self.toppings.component, discord.ui.Select)
        assert isinstance(self.size.component, discord.ui.Select)
        assert isinstance(self.notes.component, discord.ui.TextInput)

        client = interaction.client
        assert isinstance(client, MyClient)
        await client.db.create_order(
            user_id=interaction.user.id,
            shop=self.shop.component.values[0] if self.shop.component.values else "-",
            description=self.notes.component.value
            if self.notes.component.value
            else "-",
            order_name=self.boba_type.component.values[0]
            if self.boba_type.component.values
            else "-",
            size=self.size.component.values[0] if self.size.component.values else "-",
            topping=self.toppings.component.values[0]
            if self.toppings.component.values
            else "-",
            order_type="boba",
        )

        # Send the order to the Mason's dm's
        member = await interaction.client.fetch_user(int(MASON_DISCORD_ID))
        channel = await member.create_dm()
        await channel.send(view=view)
        gif = random.choice(list(jinshi_success.values()))
        await interaction.response.send_message(gif)
        await interaction.followup.send(
            "Thank you for ordering with Moober Eats, your order got sent to Mason and he is getting your food",
            ephemeral=True,
        )

    async def on_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)
        await interaction.response.send_message(
            "Mason coded something wrong T-T sorry you have to order manually",
            ephemeral=True,
        )
        gif = random.choice(list(jinshi_fail_gifs.values()))
        await interaction.followup.send(gif)


# Define a modal dialog for reporting issues or feedback
class MunchieOrderModal(discord.ui.Modal, title="Munchie Order"):
    shop = discord.ui.Label(
        text="Restaurant Location",
        description="Select yummiest food place",
        component=discord.ui.Select(
            placeholder="Where is Mason going to get food?",
            required=False,
            options=[
                discord.SelectOption(label="Tea Hill CH"),
                discord.SelectOption(label="Moge Tea CH"),
                discord.SelectOption(label="Bobo Baba Cary"),
                discord.SelectOption(label="Moge Tea Raleigh"),
                discord.SelectOption(label="Other"),
            ],
        ),
    )
    munchie_type = discord.ui.Label(
        text="Food Type",
        description="Select the type of munchie you want",
        component=discord.ui.Select(
            placeholder="what munchie are u getting?",
            required=False,
            options=[
                discord.SelectOption(label="Chicken Rice Plate"),
                discord.SelectOption(label="Yuzu Oolong"),
                discord.SelectOption(label="Superfruit Green Tea"),
                discord.SelectOption(label="Lemon Tea"),
                discord.SelectOption(label="Other"),
            ],
        ),
    )
    footer = discord.ui.TextDisplay("thank you for ordering with moober eats :)))")

    def to_view(self, interaction: discord.Interaction) -> discord.ui.LayoutView:
        # Tell the type checker what our components are...
        assert isinstance(self.shop.component, discord.ui.Select)
        assert isinstance(self.munchie_type.component, discord.ui.Select)
        assert isinstance(self.footer, discord.ui.TextDisplay)

        shop = self.shop.component.values[0] if self.shop.component.values else "-"
        munchie_type = (
            self.munchie_type.component.values[0]
            if self.munchie_type.component.values
            else "-"
        )

        view = discord.ui.LayoutView()
        container = discord.ui.Container()
        view.add_item(container)

        container.add_item(discord.ui.TextDisplay("-# New Munchie Order"))

        timestamp = discord.utils.format_dt(interaction.created_at, "F")
        footer = discord.ui.TextDisplay(
            f"-# Reported by {interaction.user} (ID: {interaction.user.id}) | {timestamp}"
        )

        if shop:
            container.add_item(discord.ui.TextDisplay(f"Restaurant: {shop}"))
        if munchie_type:
            container.add_item(discord.ui.TextDisplay(f"### Munchie: {munchie_type}"))

        container.add_item(footer)
        return view

    async def on_submit(self, interaction: discord.Interaction):
        view = self.to_view(interaction)

        client = interaction.client
        assert isinstance(client, MyClient)
        shop_component = self.shop.component
        munchie_type = self.munchie_type.component
        assert isinstance(munchie_type, discord.ui.Select)
        assert isinstance(shop_component, discord.ui.Select)

        await client.db.create_order(
            user_id=interaction.user.id,
            order_name=munchie_type.values[0],
            shop=shop_component.values[0],
            order_type="munchie",
        )

        # Send the order to the Mason's dm's
        member = await interaction.client.fetch_user(int(MASON_DISCORD_ID))
        channel = await member.create_dm()
        await channel.send(view=view)
        gif = random.choice(list(jinshi_success.values()))
        await interaction.response.send_message(gif)
        await interaction.followup.send(
            "Thank you for ordering with Moober Eats, your order got sent to Mason and he is getting your food",
            ephemeral=True,
        )

    async def on_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)
        await interaction.response.send_message(
            "Mason coded something wrong T-T sorry you have to order manually",
            ephemeral=True,
        )
        gif = random.choice(list(jinshi_fail_gifs.values()))
        await interaction.followup.send(gif)


class CustomOrderModal(discord.ui.Modal, title="Custom Order"):
    custom_order = discord.ui.Label(
        text="Custom Order",
        description="A detailed description of your custom order.",
        component=discord.ui.TextInput(
            style=discord.TextStyle.paragraph,
            placeholder="Describe your custom order here.",
            max_length=2000,
        ),
    )
    footer = discord.ui.TextDisplay("thank you for ordering with moober eats :)))")

    def to_view(self, interaction: discord.Interaction) -> discord.ui.LayoutView:
        # Tell the type checker what our components are...
        assert isinstance(self.custom_order.component, discord.ui.TextInput)

        custom_order = self.custom_order.component.value

        view = discord.ui.LayoutView()
        container = discord.ui.Container()
        view.add_item(container)

        container.add_item(discord.ui.TextDisplay("-# New Custom Order"))

        timestamp = discord.utils.format_dt(interaction.created_at, "F")
        footer = discord.ui.TextDisplay(
            f"-# Reported by {interaction.user} (ID: {interaction.user.id}) | {timestamp}"
        )

        container.add_item(discord.ui.TextDisplay(f"### Custom Order: {custom_order}"))

        container.add_item(footer)
        return view

    async def on_submit(self, interaction: discord.Interaction):
        view = self.to_view(interaction)

        client = interaction.client
        assert isinstance(client, MyClient)

        assert isinstance(self.custom_order.component, discord.ui.TextInput)

        custom_order = self.custom_order.component.value
        await client.db.create_order(
            user_id=interaction.user.id, description=custom_order, order_type="custom"
        )

        # Send the order to the Mason's dm's
        member = await interaction.client.fetch_user(int(MASON_DISCORD_ID))
        channel = await member.create_dm()
        await channel.send(view=view)
        gif = random.choice(list(jinshi_success.values()))
        await interaction.response.send_message(gif)
        await interaction.followup.send(
            "Thank you for ordering with Moober Eats, your order got sent to Mason and he is getting your food",
            ephemeral=True,
        )

    async def on_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)
        await interaction.response.send_message(
            "Mason coded something wrong T-T sorry you have to order manually",
            ephemeral=True,
        )
        gif = random.choice(list(jinshi_fail_gifs.values()))
        await interaction.followup.send(gif, ephemeral=True)


# Define a modal dialog for reporting issues or feedback
# Define a modal dialog for reporting issues or feedback
class DeliveryModal(discord.ui.Modal, title="Delivery Update"):
    def __init__(self, deliveries: list = []):
        super().__init__()
        self.delivery = discord.ui.RadioGroup(
            options=[
                discord.RadioGroupOption(
                    label=(
                        delivery["shop"]
                        + " - "
                        + delivery["order_name"]
                        + f" ({delivery['status']})"
                    ),
                    value=str(delivery["id"]),
                )
                for delivery in deliveries
            ]
        )
        self.add_item(
            discord.ui.Label(
                text="Delivery",
                description="Which order is it?",
                component=self.delivery,
            )
        )

    duration = discord.ui.Label(
        text="Duration",
        description="How far away is the food from the user.",
        component=discord.ui.Select(
            options=[
                discord.SelectOption(label="Here!"),
                discord.SelectOption(label="1 minute"),
                discord.SelectOption(label="3 minutes"),
                discord.SelectOption(label="5 minutes"),
                discord.SelectOption(label="10 minutes"),
                discord.SelectOption(label="15 minutes"),
                discord.SelectOption(label="30 minutes"),
                discord.SelectOption(label="45 minutes"),
                discord.SelectOption(label="1+ hours"),
            ],
        ),
    )
    location = discord.ui.Label(
        text="Location",
        description="Location of the delivery",
        component=discord.ui.TextInput(
            style=discord.TextStyle.paragraph,
            placeholder="where is the delivery going?",
            max_length=2000,
            required=False,
        ),
    )
    description = discord.ui.Label(
        text="Description",
        description="Notes to add to the delivery",
        component=discord.ui.TextInput(
            style=discord.TextStyle.paragraph,
            placeholder="When I use /ping, the bot does not respond at all. There are no error messages.",
            max_length=2000,
            required=False,
        ),
    )
    images = discord.ui.Label(
        text="Images",
        description="Upload any relevant images for your report (optional).",
        component=discord.ui.FileUpload(
            max_values=10,
            custom_id="report_images",
            required=False,
        ),
    )

    def to_view(
        self, interaction: discord.Interaction, old_order: dict
    ) -> discord.ui.LayoutView:
        # Tell the type checker what our components are...
        assert isinstance(self.delivery.value, str)
        shop = old_order["shop"]
        boba_type = old_order["order_name"]
        toppings = old_order["topping"]
        size = old_order["size"]
        view = discord.ui.LayoutView()
        container = discord.ui.Container()
        view.add_item(container)

        assert isinstance(self.duration.component, discord.ui.Select)
        assert isinstance(self.location.component, discord.ui.TextInput)
        assert isinstance(self.description.component, discord.ui.TextInput)
        assert isinstance(self.images.component, discord.ui.FileUpload)
        duration = self.duration.component.values[0]
        location = self.location.component.value
        description = self.description.component.value
        files = self.images.component.values

        container.add_item(discord.ui.TextDisplay(f"### Food is coming in: {duration}"))
        if location:
            container.add_item(discord.ui.TextDisplay(f">>> {location}"))

        if description:
            container.add_item(discord.ui.TextDisplay(f">>> {description}"))

        if files:
            gallery = discord.ui.MediaGallery()
            gallery.items = [
                discord.MediaGalleryItem(media=attachment.url) for attachment in files
            ]
            container.add_item(gallery)
        container.add_item(
            discord.ui.TextDisplay(
                f"Shop: {shop}\nBoba: {boba_type}\nToppings: {toppings}\nSize: {size}"
            )
        )
        return view

    async def on_submit(self, interaction: discord.Interaction):
        client = interaction.client
        assert isinstance(client, MyClient)
        delivery_value = self.delivery.value
        assert delivery_value is not None
        old_order_id = int(delivery_value)
        old_order = await client.db.get_order_by_id(old_order_id)
        assert old_order is not None

        view = self.to_view(interaction, old_order=old_order)

        # Send the order to the discord
        channel = client.get_channel(
            int(CHANNEL_ID)
        )  #  Gets channel from internal cache Sends message to channel
        if not isinstance(channel, discord.TextChannel):
            raise RuntimeError("It has to be text channel")

        await channel.send(view=view)
        duration_component = self.duration.component
        assert isinstance(duration_component, discord.ui.Select)
        if duration_component.values[0] == "Here!":
            gif = random.choice(list(delivering_gifs.values()))
            await channel.send(gif)
            delivery_value = self.delivery.value
            assert delivery_value is not None
            order_id = int(delivery_value)
            await client.db.update_order_status(id=order_id, status="delivered")
        else:
            gif = random.choice(list(maomao_success.values()))
            await channel.send(gif)

        await interaction.response.send_message(
            "Thank you for updating Joan!", ephemeral=True
        )

    async def on_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)
        await interaction.response.send_message(
            "Mason coded something wrong T-T sorry you have to just tell her manually",
            ephemeral=True,
        )


class OnlineOrderModal(discord.ui.Modal, title="Online Order modal"):
    shop = discord.ui.Label(
        text="Boba Shop Location",
        description="Select yummiest boba place",
        component=discord.ui.Select(
            placeholder="Where is Mason going to get boba?",
            required=False,
            options=[
                discord.SelectOption(label="Tea Hill CH"),
                discord.SelectOption(label="Moge Tea CH"),
                discord.SelectOption(label="Bobo Baba Cary"),
                discord.SelectOption(label="Moge Tea Raleigh"),
                discord.SelectOption(label="Other"),
            ],
        ),
    )
    footer = discord.ui.TextDisplay("thank you for ordering with moober eats :)))")

    def to_view(self, interaction: discord.Interaction) -> discord.ui.LayoutView:
        # Tell the type checker what our components are...
        assert isinstance(self.shop.component, discord.ui.Select)

        shop = self.shop.component.values[0] if self.shop.component.values else "-"

        view = discord.ui.LayoutView()
        container = discord.ui.Container()
        view.add_item(container)

        container.add_item(discord.ui.TextDisplay("-# New Boba Order"))

        timestamp = discord.utils.format_dt(interaction.created_at, "F")
        footer = discord.ui.TextDisplay(
            f"-# Reported by {interaction.user} (ID: {interaction.user.id}) | {timestamp}"
        )

        if shop:
            container.add_item(discord.ui.TextDisplay(f"Shop: {shop}"))

        container.add_item(footer)
        return view

    async def on_submit(self, interaction: discord.Interaction):

        assert isinstance(self.shop.component, discord.ui.Select)

        place_link = (
            restaurant_links["tea_hill"]
            if self.shop.component.values[0] == "Tea Hill CH"
            else (
                restaurant_links["moge_tea"]
                if self.shop.component.values[0] == "Moge Tea CH"
                else restaurant_links["bobo_baba"]
                if self.shop.component.values[0] == "Bobo Baba Cary"
                else None
            )
        )

        client = interaction.client
        assert isinstance(client, MyClient)

        gif = random.choice(list(maomao_gifs.values()))

        await interaction.response.send_message(gif)
        await interaction.followup.send(
            place_link if place_link else "i dont have a link for that store T-T.",
            ephemeral=True,
        )

    async def on_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)
        await interaction.response.send_message(
            "Mason coded something wrong T-T sorry you have to order manually",
            ephemeral=True,
        )
        gif = random.choice(list(jinshi_fail_gifs.values()))
        await interaction.followup.send(gif)


# Define a modal dialog for reporting issues or feedback
class PastDeliveryModal(discord.ui.Modal, title="Past Delivery Update"):
    def __init__(self, deliveries: list = []):
        super().__init__()
        self.delivery = discord.ui.RadioGroup(
            options=[
                discord.RadioGroupOption(
                    label=(delivery["shop"] + " - " + delivery["order_name"]),
                    value=str(delivery["id"]),
                )
                for delivery in deliveries
            ]
        )
        self.add_item(
            discord.ui.Label(
                text="Delivery",
                description="Which order is it?",
                component=self.delivery,
            )
        )

    def to_view(
        self, interaction: discord.Interaction, old_order: dict[str, str]
    ) -> discord.ui.LayoutView:
        # Tell the type checker what our components are...

        assert isinstance(self.delivery.value, str)
        shop = old_order["shop"]
        boba_type = old_order["order_name"]
        toppings = old_order["topping"]
        size = old_order["size"]
        view = discord.ui.LayoutView()
        container = discord.ui.Container()
        view.add_item(container)

        container.add_item(
            discord.ui.TextDisplay(
                f"Shop: {shop}\nBoba: {boba_type}\nToppings: {toppings}\nSize: {size}"
            )
        )

        return view

    async def on_submit(self, interaction: discord.Interaction):

        client = interaction.client
        assert isinstance(client, MyClient)
        delivery_value = self.delivery.value
        assert delivery_value is not None
        old_order_id = int(delivery_value)
        old_order = await client.db.get_order_by_id(old_order_id)
        assert old_order is not None

        await client.db.create_order(
            old_order["user_id"],
            old_order["shop"],
            old_order["order_name"],
            old_order["size"],
            old_order["topping"],
            old_order["description"],
            old_order["order_type"],
        )

        view = self.to_view(interaction, old_order=old_order)

        # Send the order to the Mason's dm's
        member = await interaction.client.fetch_user(int(MASON_DISCORD_ID))
        channel = await member.create_dm()
        await channel.send(view=view)
        gif = random.choice(list(jinshi_success.values()))
        await interaction.response.send_message(gif)
        await interaction.followup.send(
            "Thank you for ordering with Moober Eats, your order got sent to Mason and he is getting your food",
            ephemeral=True,
        )

    async def on_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)
        await interaction.response.send_message(
            "Mason coded something wrong T-T sorry you have to order manually",
            ephemeral=True,
        )
        gif = random.choice(list(jinshi_fail_gifs.values()))
        await interaction.followup.send(gif)
