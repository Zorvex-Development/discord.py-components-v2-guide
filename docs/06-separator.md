# 06 — Separator: dividers and whitespace

`discord.ui.Separator` creates a visual break between items. It can draw a divider and can apply a small or large spacing treatment.

## Visible divider

```python
panel.add_item(discord.ui.TextDisplay("### Ticket details"))
panel.add_item(discord.ui.Separator())
panel.add_item(discord.ui.TextDisplay("**Status:** Open\n**Priority:** Normal"))
```

## Spacing-only separator

```python
panel.add_item(discord.ui.Separator(divider=False, spacing=discord.SeparatorSpacing.large))
```

Use a visible line when two sections need clear separation; use whitespace when the visual hierarchy is already clear and another line would be too noisy.

## Spacing values

The library exposes `discord.SeparatorSpacing.small` and `discord.SeparatorSpacing.large`. Exact rendering is controlled by Discord clients, so treat it as a layout hint rather than a pixel-perfect CSS measurement.

## Reusable layout pattern

```python
panel.add_item(discord.ui.TextDisplay("# Music session"))
panel.add_item(discord.ui.Separator())
panel.add_item(discord.ui.TextDisplay("**Now playing**\nExample track"))
panel.add_item(discord.ui.Separator(divider=False, spacing=discord.SeparatorSpacing.large))
panel.add_item(discord.ui.TextDisplay("**Queue**\n3 tracks remaining"))
```

## Pitfalls

- Avoid separating every tiny line; too many dividers make the message harder to scan.
- A separator changes presentation, not permissions or interaction behaviour.
- Check the layout in Discord's actual clients rather than assuming a fixed pixel height.
