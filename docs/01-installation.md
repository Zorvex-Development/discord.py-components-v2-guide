# 01 — Installation and project setup

## Requirements

- Python 3.8 or newer according to the current `discord.py` package metadata; use a currently supported Python release for new projects.
- `discord.py` 2.6.0 or newer for Components V2. This guide was written against 2.7.1.
- A Discord application and bot user created in the Discord Developer Portal.
- A token stored outside source control.

## Create a project

```text
my-discord-bot/
├── .env
├── .gitignore
├── bot.py
└── requirements.txt
```

Create and activate a virtual environment:

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1
python -m pip install -U discord.py python-dotenv
```

A virtual environment keeps one project's dependencies separate from system Python. This matters most when working on servers or distributions that prevent global package installs.

## Verify the installed library

```bash
python -c "import discord; print(discord.__version__); print(hasattr(discord.ui, 'LayoutView'))"
```

The version should be at least `2.6.0`; the second value should print `True`. If it does not, you may be running a different environment or an outdated package. Also check that your own project does not contain a file named `discord.py`, which can shadow the installed package.

## Minimal environment-based startup

`.env`:

```dotenv
DISCORD_TOKEN=put_your_real_token_here
```

`bot.py`:

```python
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
if not token:
    raise RuntimeError("DISCORD_TOKEN is missing; set it in .env or the host environment")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (discord.py {discord.__version__})")

bot.run(token)
```

Never paste your token into a public repository or screenshots. If it leaks, reset it immediately in the Developer Portal. Add `.env` to `.gitignore` before the first commit.

## Intents and permissions are different

Gateway intents control which event data the bot receives. Guild permissions control what the bot can do in a server. A Components V2 panel usually needs no privileged intent by itself, but commands that inspect message content, members, or presences may require additional configuration. Ask only for the permissions the bot actually needs.

## Slash commands versus prefix commands

Components V2 is a message layout feature, not a command-registration system. The examples use prefix commands for quick setup and interactions for callbacks; the same `LayoutView` can be sent from a slash-command handler. If using application commands, remember to sync the command tree in the way your bot architecture expects.
