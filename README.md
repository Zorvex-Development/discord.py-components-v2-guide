# ZorveX Development — Discord.py Components V2 Handbook

A practical, independently written guide to building modern Discord message layouts with **Python** and **discord.py**. This project is published under the ZorveX Development name and is organised as a set of focused, linkable documents rather than one giant tutorial.

> **API baseline:** `discord.py` 2.7.1. Components V2 support was introduced in `discord.py` 2.6.0. Confirm API details against the official documentation when upgrading, because Discord and its libraries evolve independently of tutorial code.

## What this covers

- Components V2 concepts, message rules, and the `discord.ui.LayoutView` root.
- Containers, text displays, sections, thumbnails, separators, buttons, rows, and select menus.
- Media galleries and inline file attachments.
- Interaction acknowledgement, editing, ephemeral replies, modal handoff, state, persistence, and authorization.
- Migration from embeds and legacy `discord.ui.View` layouts.
- Production-oriented examples and troubleshooting.

## Quick start

Create a virtual environment and install the supported PyPI package:

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -U discord.py
```

Components V2 needs `discord.py` **2.6.0 or newer**. Check what is installed:

```bash
python -c "import discord; print(discord.__version__)"
```

Copy `.env.example` to `.env`, set `DISCORD_TOKEN`, and run an example:

```bash
python examples/quick_start.py
```

The examples assume you've created an application and bot in the Discord Developer Portal. Invite the bot with the permissions required by the features you test. Never commit a real token.

## Documentation map

| File | Topic |
|---|---|
| [00 — Overview](docs/00-overview.md) | Mental model and where V2 fits |
| [01 — Installation](docs/01-installation.md) | Python, dependency, bot setup |
| [02 — LayoutView and message rules](docs/02-layoutview-and-message-rules.md) | Root layout, flags, limitations |
| [03 — TextDisplay](docs/03-text-display.md) | Markdown and readable text structure |
| [04 — Container](docs/04-container.md) | Grouping and accent colours |
| [05 — Section and Thumbnail](docs/05-sections-and-thumbnails.md) | Side-by-side content and accessories |
| [06 — Separator](docs/06-separator.md) | Dividers and spacing |
| [07 — ActionRow and buttons](docs/07-action-rows-and-buttons.md) | Button layouts and callbacks |
| [08 — Select menus](docs/08-select-menus.md) | String, user, role, channel, mentionable selects |
| [09 — MediaGallery](docs/09-media-gallery.md) | Image/video gallery layouts |
| [10 — File component](docs/10-file-component.md) | Inline attachments and buffers |
| [11 — Interaction lifecycle](docs/11-interaction-lifecycle.md) | Reply, defer, edit, modal patterns |
| [12 — Persistent views and state](docs/12-persistent-views-and-state.md) | Restart-safe components |
| [13 — Security and validation](docs/13-security-and-validation.md) | Permission checks and untrusted input |
| [14 — Migration from embeds](docs/14-migration-from-embeds.md) | Incremental migration guide |
| [15 — Production patterns](docs/15-production-patterns.md) | Complete architecture examples |
| [16 — Troubleshooting](docs/16-troubleshooting.md) | Common errors and fixes |
| [17 — Limits and compatibility](docs/17-limits-and-compatibility.md) | Fast-reference table and official references |
| [18 — Modal components in 2.7](docs/18-modal-components-in-2.7.md) | Modern labels, file uploads, radio and checkbox inputs |
| [Contributing](CONTRIBUTING.md) | How to improve the guide |
| [License](LICENSE.md) | ZorveX License terms and required publication placeholders |

## Smallest useful example

```python
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

class WelcomeLayout(discord.ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=180)
        panel = discord.ui.Container(accent_color=discord.Colour.blurple())
        panel.add_item(discord.ui.TextDisplay("# Welcome\nThis message uses Components V2."))
        self.add_item(panel)

@bot.command()
async def panel(ctx: commands.Context):
    await ctx.send(view=WelcomeLayout())

bot.run(os.environ["DISCORD_TOKEN"])
```

For real usage, read [installation](docs/01-installation.md) first and replace the illustrative token handling with the `.env` pattern documented there.

## Important behavioural difference

A V2 message is laid out with components. Do not try to combine its `LayoutView` with legacy message `content=`, `embed=`/`embeds=`, stickers, or polls in the same message payload. Put visible text in `discord.ui.TextDisplay` components. Traditional `discord.ui.View` and embeds remain available for other messages in the same bot; migration is incremental, not bot-wide.

## Upstream and reference documentation

- [discord.py documentation](https://discordpy.readthedocs.io/en/stable/)
- [Interactions and UI API](https://discordpy.readthedocs.io/en/stable/interactions/api.html)
- [discord.py changelog](https://discordpy.readthedocs.io/en/stable/whats_new.html)
- [discord.py on PyPI](https://pypi.org/project/discord.py/)
- [Discord Components Reference](https://discord.com/developers/docs/components/overview)

This handbook is not affiliated with Discord or the maintainers of discord.py. Names of libraries and services remain with their respective owners.
