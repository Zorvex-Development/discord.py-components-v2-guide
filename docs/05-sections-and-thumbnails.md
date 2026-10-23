# 05 — Sections and accessories

A `discord.ui.Section` places one or more text displays beside an accessory on the right. Common accessories are `discord.ui.Thumbnail` or a button. It is well suited to a user summary, track row, ticket opener details, or a compact status item.

## Text with an avatar thumbnail

```python
section = discord.ui.Section(
    accessory=discord.ui.Thumbnail(media=member.display_avatar.url)
)
section.add_item(discord.ui.TextDisplay(f"## {member.display_name}"))
section.add_item(discord.ui.TextDisplay(f"Member ID: `{member.id}`"))
panel.add_item(section)
```

Use a valid media URL for the thumbnail. If an asset may be missing, decide how the surrounding text should look when the thumbnail is unavailable; do not assume every guild, user, or application has an icon.

## Guild icon fallback

```python
if interaction.guild and interaction.guild.icon:
    accessory = discord.ui.Thumbnail(media=interaction.guild.icon.url)
    section = discord.ui.Section(accessory=accessory)
    section.add_item(discord.ui.TextDisplay("# Guild settings"))
    section.add_item(discord.ui.TextDisplay("Choose a setting to review."))
    panel.add_item(section)
else:
    panel.add_item(discord.ui.TextDisplay("# Guild settings"))
    panel.add_item(discord.ui.TextDisplay("Choose a setting to review."))
```

The fallback matters in DMs and in servers that do not have an uploaded icon.

## Button accessory

For one compact action, a button can be the accessory:

```python
refresh = discord.ui.Button(
    label="Refresh",
    style=discord.ButtonStyle.secondary,
    custom_id="zorvex:status:refresh",
)
refresh.callback = self.refresh_status

section = discord.ui.Section(accessory=refresh)
section.add_item(discord.ui.TextDisplay("**System status**\nLast checked recently."))
panel.add_item(section)
```

The callback must be an async callable compatible with the button's interaction callback. A button accessory is still interactive, so it needs the same validation, acknowledgement, and authorization checks as a button placed in an action row.

## Keep the text layout sensible

- Put the primary label first and details below it.
- Do not place important information only in the thumbnail.
- Use an accessory button for one short action, not a row of several controls.
- If the accessory is optional, create a text-only layout as a fallback.
