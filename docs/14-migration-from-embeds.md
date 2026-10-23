# 14 — Migrating from embeds and classic Views

Components V2 is opt-in at the message level. Migrate one panel at a time, compare the results, and keep legacy messages working while you update the code that creates them.

## Conversion map

| Existing message feature | V2 approach |
|---|---|
| Embed title | Heading in `ui.TextDisplay` |
| Embed description | One or more text displays |
| Embed fields | Separate text blocks, sections, or containers |
| Embed colour | `ui.Container(accent_color=...)` |
| Embed image | `ui.MediaGallery` |
| Embed thumbnail | `ui.Section(accessory=ui.Thumbnail(...))` |
| Embed footer | A final, smaller text display (Discord controls actual typography) |
| Classic view buttons | Button items placed in `ui.ActionRow` inside `LayoutView` |

The new layout is not a byte-for-byte replacement of an embed. Test wrapping, mobile rendering, media behaviour, and the resulting accessibility/readability.

## Migration steps

1. **Identify one message.** Start with a static informational panel rather than a critical ticket or moderation flow.
2. **Move text first.** Create `LayoutView` and `TextDisplay` blocks without interactivity.
3. **Group related sections.** Add containers and separators only where they help scanning.
4. **Move media.** Use a gallery or thumbnail accessory and add fallback text.
5. **Rebuild actions.** Place buttons/selects into action rows and port callback validation.
6. **Update the send call.** Remove the old embed and `content` arguments from the V2 send payload.
7. **Test failures.** Check missing avatars, deleted roles/channels, expired state, permissions, and response timeout paths.
8. **Roll out gradually.** Keep a rollback path until the new panel has been tested on the actual Discord clients your users rely on.

## Before and after

Legacy version:

```python
embed = discord.Embed(
    title="Queue status",
    description="**Now playing:** Example track\n**Queued:** 4",
    colour=discord.Colour.blurple(),
)
await channel.send(embed=embed, view=classic_view)
```

V2 version:

```python
layout = discord.ui.LayoutView(timeout=180)
panel = discord.ui.Container(accent_color=discord.Colour.blurple())
panel.add_item(discord.ui.TextDisplay("# Queue status"))
panel.add_item(discord.ui.Separator())
panel.add_item(discord.ui.TextDisplay("**Now playing:** Example track\n**Queued:** 4"))
layout.add_item(panel)
await channel.send(view=layout)
```

The `classic_view` in the old call cannot simply be attached to the new V2 message. Recreate its actions using supported children of `LayoutView` and `ActionRow`.

## Editing an existing message

When converting a legacy message in place, clear old content and embeds during the edit. The details of editing depend on the current library version and the message's existing components. Always test against a disposable message first.

## Avoid all-at-once rewrites

Do not migrate every bot message merely because V2 exists. Classic embeds are still valid and may be the better choice for a simple data presentation. Choose V2 when the desired layout benefits from component-based composition or its supported interactive structure.
