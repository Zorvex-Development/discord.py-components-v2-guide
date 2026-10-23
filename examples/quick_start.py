"""A minimal Components V2 example for discord.py 2.6+.

Set DISCORD_TOKEN in the environment or in a local .env file before running.
"""

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("Set DISCORD_TOKEN in your environment or .env file")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


class WelcomeLayout(discord.ui.LayoutView):
    def __init__(self) -> None:
        super().__init__(timeout=180)
        panel = discord.ui.Container(accent_color=discord.Colour.from_rgb(95, 0, 255))
        panel.add_item(discord.ui.TextDisplay("# Welcome to the server"))
        panel.add_item(discord.ui.Separator())
        panel.add_item(
            discord.ui.TextDisplay(
                "This message uses Discord Components V2.\n"
                "Use `!panel` to display it again."
            )
        )

        hello = discord.ui.Button(
            label="Say hello",
            style=discord.ButtonStyle.primary,
            custom_id="zorvex:quickstart:hello",
        )
        hello.callback = self.say_hello
        panel.add_item(discord.ui.ActionRow(hello))
        self.add_item(panel)

    async def say_hello(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            f"Hello, {interaction.user.mention}!", ephemeral=True
        )


@bot.command(name="panel")
async def send_panel(ctx: commands.Context) -> None:
    await ctx.send(view=WelcomeLayout())


@bot.event
async def on_ready() -> None:
    print(f"Ready as {bot.user} | discord.py {discord.__version__}")


bot.run(TOKEN)
