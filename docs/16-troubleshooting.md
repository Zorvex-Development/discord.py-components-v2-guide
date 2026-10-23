# 16 — Troubleshooting

## `AttributeError: module 'discord.ui' has no attribute 'LayoutView'`

Your active Python environment likely has `discord.py` older than 2.6.0, or you imported a different module. Check the version and path:

```bash
python -c "import discord; print(discord.__version__); print(discord.__file__)"
python -m pip show discord.py
python -m pip install -U discord.py
```

Also make sure the project does not contain a local file named `discord.py` or a folder named `discord/` shadowing the installed library.

## `ModuleNotFoundError: No module named 'discord'`

Install the package into the same Python environment that runs the bot:

```bash
python -m pip install -U discord.py
```

Do not use a bare `pip` if it points to a different interpreter. `python -m pip` ties the package installation to the chosen executable.

## Discord rejects a message with an invalid form body

Check component placement and message restrictions. Common causes include an item under an unsupported parent, too many components, a row with the wrong child composition, legacy `content`/embeds being sent with V2, or invalid media/attachment references. Reduce the layout to one `TextDisplay`, then add components back one at a time.

## `InteractionResponded` or the interaction fails to respond

The callback probably tried to send more than one initial response. Use `interaction.response` once; after defer/respond, use a follow-up or edit path. For slow operations, acknowledge promptly with `defer()` and continue the work after that.

## The button is visible but does nothing

A visible button does not guarantee it has a callback. For a manually built button, assign an async callback before sending it. For a persistent view, use stable `custom_id` values and register the view during startup. Link buttons navigate to a URL and do not invoke a callback.

## Components stop working after a restart

Check `timeout=None`, stable `custom_id` values, `bot.add_view(...)` registration during startup, and whether the callback code still recognises IDs from the older deployed version. Store application state in durable storage instead of only in Python objects.

## The UI references a missing attachment

The `attachment://` name must match the upload's filename exactly. Ensure the corresponding `discord.File` is passed to the same send/edit request and that a `BytesIO` stream is positioned at the beginning before upload.

## Thumbnail or gallery does not render

Check that you supplied a URL in the correct format, the host is reachable by Discord, the URL has not expired, and the current media item constructor matches your pinned `discord.py` version. Try a known stable public asset and add text fallback.

## Select menu callback receives unexpected values

Treat the interaction data as untrusted. Validate selected values against an allow-list and re-check whether the selected object still exists and is allowed in the current guild. For entity selects, use the resolved objects available through the relevant component type when supported by your library version.

## Enable logs while debugging

```python
import logging

logging.basicConfig(level=logging.INFO)
```

For deeper troubleshooting, see the official [discord.py logging guide](https://discordpy.readthedocs.io/en/stable/logging.html) and [interactions API reference](https://discordpy.readthedocs.io/en/stable/interactions/api.html). Avoid logging secrets or private interaction data.
