# 00 — Components V2: the mental model

Components V2 is Discord's component-based message layout system. In `discord.py`, the user-facing entry point for sending these layouts is `discord.ui.LayoutView`.

It is useful when a bot needs dashboard-like panels, multi-section status cards, ticket controls, interactive menus, image galleries, or structured messages that would otherwise be built from embeds and ordinary action rows.

## The hierarchy

```text
LayoutView                         Root object passed as view=
├── TextDisplay                    Markdown text block
├── Container                      Optional visual group
│   ├── TextDisplay
│   ├── Separator                  Divider or whitespace
│   ├── Section                    Text plus an accessory
│   │   └── Thumbnail or Button
│   ├── MediaGallery               Media tiles
│   ├── File                       Inline attachment display
│   └── ActionRow                  Buttons or one select menu
└── Container                     Another top-level group
```

The tree is a helpful mental model, not permission to nest every item everywhere. Each class has allowed parent locations. For example, containers belong at the top-level of a `LayoutView`; a container cannot contain another container.

## Components V2 versus the legacy UI

| Legacy pattern | Components V2 pattern |
|---|---|
| `discord.Embed(title=..., description=...)` | `ui.TextDisplay` blocks arranged in a `ui.LayoutView` |
| `embed.color` | `ui.Container(accent_color=...)` |
| `embed.set_image(...)` | `ui.MediaGallery` |
| `embed.set_thumbnail(...)` | `ui.Section` with `ui.Thumbnail` accessory |
| `discord.ui.View` for classic buttons | `discord.ui.LayoutView` for V2 content and controls |

This is a mapping, not a mandatory migration. A bot may use classic embeds/views for some messages and V2 layouts for others.

## Three design rules

1. **Start with the content hierarchy.** Decide which items are headings, supporting text, media, dividers, and actions before constructing objects.
2. **Separate presentation from behaviour.** Layout classes should explain the interface; callbacks should validate input, check permissions, do the work, and acknowledge the interaction.
3. **Build for narrow screens.** Keep headings short, avoid dense walls of text, and group related actions logically. Desktop previews are not enough.

## API baseline

Components V2 support was added in `discord.py` 2.6.0. This handbook uses APIs available in `discord.py` 2.7.1 unless a section identifies a feature as version-specific. For the latest version, check [PyPI](https://pypi.org/project/discord.py/) and the [stable API reference](https://discordpy.readthedocs.io/en/stable/interactions/api.html).
