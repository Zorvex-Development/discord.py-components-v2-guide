"""A small interactive support-category panel.

This example demonstrates component layout and validates selected values.
It does not implement ticket creation or a database.
"""

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("Set DISCORD_TOKEN in your environment or .env file")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())
ALLOWED_CATEGORIES = {"general", "technical", "billing"}


class SupportPanel(discord.ui.LayoutView):
    def __init__(self) -> None:
        super().__init__(timeout=180)
        panel = discord.ui.Container(accent_color=discord.Colour.blurple())
        panel.add_item(discord.ui.TextDisplay("# Support centre"))
        panel.add_item(discord.ui.TextDisplay("Choose a category to continue."))
        panel.add_item(discord.ui.Separator())

        category = discord.ui.Select(
            placeholder="Select a support category",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(label="General", value="general"),
                discord.SelectOption(label="Technical issue", value="technical"),
                discord.SelectOption(label="Billing", value="billing"),
            ],
            custom_id="zorvex:support:category:v1",
        )
        self.category_select = category
        category.callback = self.category_selected
        panel.add_item(discord.ui.ActionRow(category))
        self.add_item(panel)

    async def category_selected(self, interaction: discord.Interaction) -> None:
        values = self.category_select.values
        if len(values) != 1 or values[0] not in ALLOWED_CATEGORIES:
            await interaction.response.send_message(
                "The selected category is invalid. Please try again.", ephemeral=True
            )
            return

        selected = values[0]
        await interaction.response.send_message(
            f"You selected **{selected}**.\n"
            "Connect this handler to your ticket service to create a real ticket.",
            ephemeral=True,
        )


@bot.command(name="supportpanel")
async def send_support_panel(ctx: commands.Context) -> None:
    await ctx.send(view=SupportPanel())


@bot.event
async def on_ready() -> None:
    print(f"Ready as {bot.user}")


bot.run(TOKEN)
