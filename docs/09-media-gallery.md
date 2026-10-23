# 09 — MediaGallery

`discord.ui.MediaGallery` displays a collection of media tiles in a Components V2 message. Use it for artwork, preview images, a collection of related screenshots, or a compact gallery of a few assets.

## Display one image

```python
gallery = discord.ui.MediaGallery(
    discord.MediaGalleryItem(media="https://example.com/cover.png")
)
panel.add_item(gallery)
```

## Display several images

```python
gallery = discord.ui.MediaGallery(
    discord.MediaGalleryItem(media="https://example.com/one.png", description="First preview"),
    discord.MediaGalleryItem(media="https://example.com/two.png", description="Second preview"),
    discord.MediaGalleryItem(media="https://example.com/three.png", description="Third preview"),
)
panel.add_item(gallery)
```

The exact fields accepted by each media item are defined by your installed `discord.py` version. Confirm them in the [MediaGallery API reference](https://discordpy.readthedocs.io/en/stable/interactions/api.html).

## Local uploaded images

For a local image, send it as an attachment and reference it using the supported `attachment://filename` media URI where allowed. The attached filename must match exactly. For inline files as document-like content, use the `ui.File` component instead; see [File component](10-file-component.md).

## Limits and resilient design

- Discord documents a maximum of 10 media items in a gallery.
- Remote URLs must be accessible to Discord; a local filesystem path is not a usable remote URL.
- Do not assume external image hosts always stay online.
- Add meaningful text outside the image so the message still communicates its purpose if media is not visible.
- Check media source rights before redistributing user or third-party artwork.

## Example: profile preview

```python
panel.add_item(discord.ui.TextDisplay(f"# {member.display_name}'s avatar"))
panel.add_item(discord.ui.MediaGallery(
    discord.MediaGalleryItem(media=member.display_avatar.url)
))
```

This is presentation only. Avatar URLs are dynamic; if you store a URL for later, consider whether it may change or expire and resolve it again when building the message.
