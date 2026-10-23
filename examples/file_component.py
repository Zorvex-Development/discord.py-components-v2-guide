"""Send a generated text attachment referenced by a V2 File component."""

import io
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("Set DISCORD_TOKEN in your environment or .env file")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())


@bot.command(name="exportexample")
async def export_example(ctx: commands.Context) -> None:
    filename = "zorvex-example-export.txt"
    contents = (
        "ZorveX Development — Components V2 sample export\n"
        "This is demonstration data, not a real server transcript.\n"
    )
    payload = io.BytesIO(contents.encode("utf-8"))
    upload = discord.File(payload, filename=filename)

    view = discord.ui.LayoutView(timeout=180)
    panel = discord.ui.Container(accent_color=discord.Colour.blurple())
    panel.add_item(discord.ui.TextDisplay("# Export ready"))
    panel.add_item(discord.ui.TextDisplay("The example file is attached below."))
    panel.add_item(discord.ui.File(media=f"attachment://{filename}"))
    view.add_item(panel)

    await ctx.send(view=view, file=upload)


bot.run(TOKEN)
