# 04 — Container: group and style the layout

`discord.ui.Container` groups related content and can apply an accent colour or spoiler presentation. It is the closest V2 equivalent to a visually grouped card, but it is not an embed and does not inherit embed fields.

## Create a panel

```python
import discord

class HelpLayout(discord.ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=180)
        panel = discord.ui.Container(accent_color=discord.Colour.from_rgb(95, 0, 255))
        panel.add_item(discord.ui.TextDisplay("# Help centre"))
        panel.add_item(discord.ui.Separator())
        panel.add_item(discord.ui.TextDisplay("Choose an action below to continue."))
        self.add_item(panel)
```

The library accepts both `accent_color` and `accent_colour` spellings. Choose one spelling and use it consistently in your codebase.

## Suggested colour roles

```python
discord.Colour.blurple()
discord.Colour.green()
discord.Colour.red()
discord.Colour.from_rgb(95, 0, 255)
```

Use accent colour to communicate a small number of intentional states, such as neutral, success, warning, or danger. Colour alone should never carry the only meaning because themes, contrast, and accessibility vary.

## Multiple containers

A `LayoutView` can contain several separate containers. This is useful for a dashboard where the overview and controls should remain distinct:

```python
layout = discord.ui.LayoutView()
summary = discord.ui.Container(accent_color=discord.Colour.blurple())
summary.add_item(discord.ui.TextDisplay("# Server overview"))
summary.add_item(discord.ui.TextDisplay("Members: **420**"))

health = discord.ui.Container(accent_color=discord.Colour.green())
health.add_item(discord.ui.TextDisplay("### Health\nAll systems operational."))

layout.add_item(summary)
layout.add_item(health)
```

## Valid children and nesting

A container can include supported content and layout items such as text displays, separators, sections, media galleries, file components, and action rows. Do **not** nest one container inside another container. Place each container as a child of the `LayoutView`.

## Spoilers

`discord.ui.Container(..., spoiler=True)` marks the container as spoiler content. Use it only when spoiler treatment makes sense for the actual content; it is not a security or access-control boundary.

## Design advice

- Give each container one purpose.
- Use headings and separator patterns consistently.
- Avoid excessive colour changes in a single message.
- Check layout and contrast on mobile and desktop.
- Keep permissions and actions in callback code, not in the container's visual design.
