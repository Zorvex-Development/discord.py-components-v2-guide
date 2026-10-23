# 03 — TextDisplay: message content without embeds

`discord.ui.TextDisplay` renders Markdown-formatted text inside a Components V2 layout. Use it for titles, descriptions, labels, status summaries, instructions, timestamps, and compact records.

## Basic construction

```python
panel = discord.ui.Container()
panel.add_item(discord.ui.TextDisplay("# Music dashboard"))
panel.add_item(discord.ui.TextDisplay("**Track:** Example track\n**State:** Playing"))
```

Discord Markdown works inside text displays, including headings, emphasis, inline code, code blocks, blockquotes, links, spoilers, emoji, mentions, and timestamps. Use the syntax documented by Discord rather than expecting arbitrary HTML or CSS to work.

## Arrange content into separate blocks

Instead of making a single wall of text, create blocks for the main title, the key status, and supporting details:

```python
panel.add_item(discord.ui.TextDisplay("# Queue overview"))
panel.add_item(discord.ui.Separator())
panel.add_item(discord.ui.TextDisplay("**Now playing**\nExample Artist — Example Track"))
panel.add_item(discord.ui.TextDisplay("**Up next**\n1. Track A\n2. Track B"))
```

Separate blocks make the structure easier to scan, but all of the text still counts toward the layout's aggregate content budget. Keep labels short and validate long dynamic content before constructing the message.

## Timestamps and mentions

```python
import discord

now = int(discord.utils.utcnow().timestamp())
text = discord.ui.TextDisplay(
    f"Started <t:{now}:R>\n"
    f"Absolute time: <t:{now}:F>\n"
    f"Requested by {user.mention}"
)
```

Mention rendering does not automatically mean every role/user will be pinged. Configure allowed mentions deliberately on the send call if your application allows dynamic, untrusted content. See [security and validation](13-security-and-validation.md).

## User-provided text

Treat names, search queries, external API responses, and user-submitted descriptions as data, not trusted Markdown. If a value may contain mentions, links, or Markdown, decide whether to sanitise it, escape formatting, truncate it, or display it in code formatting. Use the library's allowed-mentions controls where needed to prevent unexpected pings.

## Length and splitting

Do not assume that every text block has its own unlimited budget. The total text across the layout is constrained. Prefer pagination, a follow-up message, an attached text file, or a link to longer content rather than filling a single panel with thousands of characters.

## Common mistakes

- Passing legacy `content=` along with a V2 view.
- Treating `TextDisplay` as a replacement for arbitrary HTML or embed field layout.
- Inserting unescaped external content into Markdown without considering mentions and links.
- Building an enormous layout without checking aggregate content length.
