# 17 — Limits, compatibility, and reference links

Discord enforces component and message payload rules. Limits may change, and library validations can be updated independently from the Discord client UI. For release-sensitive details, use the official references linked below rather than treating this summary as a substitute for the API documentation.

## Useful limits to design around

| Area | Design constraint |
|---|---|
| V2 layout root | Use `discord.ui.LayoutView` |
| Component count | Plan for Discord's 40-component overall limit per message layout, including nested components |
| Action row | Up to 5 buttons or 1 select menu |
| String select options | Up to 25 options |
| Media gallery | Up to 10 media items |
| Text content | Respect the layout-wide text budget; avoid packing all copy into one message |
| Components V2 version | Requires `discord.py` 2.6.0+ |
| Current baseline used here | `discord.py` 2.7.1; check PyPI for newer releases |

The aggregate text budget and component counting details can be refined by upstream API changes. Check the versioned API/changelog before relying on boundary values in production.

## Parent compatibility at a glance

- `LayoutView` is the root view for Components V2.
- `Container` can be used as a top-level layout item; it cannot be nested in another container.
- `ActionRow` contains buttons or a single select menu and may be placed where the V2 layout schema permits it.
- `TextDisplay`, `Section`, `Separator`, `MediaGallery`, and `File` each have specific allowed parent positions. Do not assume all children can be placed at the root or in every other component.
- `discord.ui.Modal` is a separate interaction surface. It is opened from an interaction response, not inserted into the message layout tree.

## Official sources

1. [discord.py stable Interactions API](https://discordpy.readthedocs.io/en/stable/interactions/api.html)
2. [discord.py latest changelog](https://discordpy.readthedocs.io/en/stable/whats_new.html)
3. [discord.py package and releases on PyPI](https://pypi.org/project/discord.py/)
4. [Discord Components Overview](https://discord.com/developers/docs/components/overview)
5. [Discord Components Reference](https://discord.com/developers/docs/components/reference)
6. [discord.py GitHub repository](https://github.com/Rapptz/discord.py)

## Version pinning

For a reusable bot deployment, pin a tested version or a controlled version range in your dependency file. Upgrade on purpose, run syntax and smoke tests, and inspect the changelog before publishing. Do not blindly install the newest development branch just to obtain a feature already released to PyPI.
