# 02 — `LayoutView` and V2 message rules

## Why `LayoutView` is the root

A `discord.ui.LayoutView` tells `discord.py` to serialize the message using Components V2. Add top-level layout or content items to it, then pass the view as `view=` when sending or editing a message.

```python
import discord

layout = discord.ui.LayoutView(timeout=180)
layout.add_item(discord.ui.TextDisplay("# Service status\nAll systems are operational."))
await channel.send(view=layout)
```

The example belongs inside an async command or event handler. `LayoutView` is not itself a visible card; its children define what Discord renders.

## A basic container layout

```python
import discord

class StatusLayout(discord.ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=180)
        panel = discord.ui.Container(accent_color=discord.Colour.blurple())
        panel.add_item(discord.ui.TextDisplay("# Status panel"))
        panel.add_item(discord.ui.Separator())
        panel.add_item(discord.ui.TextDisplay("**API:** Operational\n**Queue:** Normal"))
        self.add_item(panel)
```

Send it with `await channel.send(view=StatusLayout())` or from an interaction with `await interaction.response.send_message(view=StatusLayout())`.

## What cannot be mixed into the same V2 message

When sending a Components V2 layout, do not combine the same message payload with legacy `content=`, `embed=`/`embeds=`, stickers, or polls. Put user-visible copy into one or more `ui.TextDisplay` elements. An ordinary attachment can still be uploaded when a V2 `ui.File` references the attachment by filename.

Incorrect:

```python
await channel.send(content="Hello", view=StatusLayout())
await channel.send(embed=discord.Embed(title="Status"), view=StatusLayout())
```

Correct:

```python
layout = discord.ui.LayoutView()
layout.add_item(discord.ui.TextDisplay("# Hello\nStatus is ready."))
await channel.send(view=layout)
```

## Sending ephemeral layouts

Ephemeral replies are visible only to the invoking user and are useful for private results, error details, previews, and user-specific menus.

```python
await interaction.response.send_message(view=StatusLayout(), ephemeral=True)
```

An ephemeral response cannot be made public later. Choose visibility based on the audience of the information, not as a way to hide a permission mistake.

## Editing an existing message

When converting an older message to V2, clear its legacy content and embeds during the edit:

```python
await message.edit(content=None, embeds=[], view=StatusLayout())
```

Read the current method signature and test this in a non-critical channel first. A conversion is not merely a visual change; Components V2 changes the valid fields for that message.

## Object identifiers

Some UI items expose an `id` used to identify the component object within a message layout. Interactive buttons and selects use `custom_id` to route interactions. These are different concepts; do not substitute one for the other.

## Practical checklist

- Every V2 message is sent with a `LayoutView`.
- Every item is placed in a supported parent position.
- Visible writing is made from `TextDisplay` components.
- No legacy content or embed is passed in the same V2 payload.
- If editing a legacy message, clear old content/embeds explicitly.
- Test both public and ephemeral response paths.
