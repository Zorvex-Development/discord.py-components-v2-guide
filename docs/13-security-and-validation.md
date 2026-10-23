# 13 — Security, permissions, and validation

A polished panel is not a security boundary. Anyone who can interact with a visible control may attempt to submit inputs you did not expect. Server-side callbacks must verify identity, scope, permissions, and state.

## Check the actor before changing anything

Example shape for an administrative action:

```python
async def delete_panel_action(self, interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message("This action is server-only.", ephemeral=True)
        return

    permissions = getattr(interaction.user, "guild_permissions", None)
    if permissions is None or not permissions.manage_messages:
        await interaction.response.send_message("You do not have permission to do that.", ephemeral=True)
        return

    # Re-check the target record and its current state before mutation.
    await interaction.response.send_message("Permission check passed.", ephemeral=True)
```

Use the permission that matches the action, not `administrator` as a shortcut for every feature. Check that a target belongs to the expected guild and that the bot itself has the required permission.

## Validate select values

Never assume a submitted menu value is valid simply because the UI originally listed it. Check values against an allow-list or resolve the target entity from the current guild and verify it is still eligible. Items may have been deleted or permissions may have changed since the message was sent.

## Control mentions

If dynamic or user-supplied content is placed in `TextDisplay`, be intentional about mention notifications. Configure `allowed_mentions` on the message send or edit method, for example by disabling mentions when you do not intend to ping anyone:

```python
safe_mentions = discord.AllowedMentions.none()
await channel.send(view=layout, allowed_mentions=safe_mentions)
```

Confirm that the relevant send/edit call and library version accept the argument for the V2 payload you use. Mention parsing and Markdown display are not the same thing.

## Treat URLs and uploaded files as untrusted

- Do not fetch arbitrary URLs from a user without SSRF controls, host allow-lists, timeouts, and size limits.
- Do not assume the URL displayed by a message is safe because it appears in a thumbnail or gallery.
- Do not put secrets in attachment filenames, custom IDs, logs, or public transcripts.
- Limit generated file size and prevent path traversal when choosing a local file.

## Rate limits and duplicate actions

Disable buttons or update the UI after an operation when appropriate, but do not depend on a disabled button as your only protection. Use idempotency keys, transactions, locks, or state checks for operations where duplicate processing would be costly.

## Error handling

Return user-friendly messages to Discord and keep full technical diagnostics in structured logs. Avoid swallowing all exceptions silently. Do not send stack traces, environment variables, SQL statements with private data, or API credentials back to an interaction.

## Operational checklist

- Actor permissions are checked in the callback.
- Target objects are re-resolved and verified.
- User-supplied strings and menu values are validated.
- Mentions are controlled deliberately.
- External requests have timeouts and size limits.
- Durable state is stored outside the UI object.
- Sensitive logs and transcripts are access-controlled.
