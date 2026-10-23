# 11 — Interaction lifecycle, responses, and modals

Components are only interactive when the bot handles their interaction events. Every button or select interaction must receive an acknowledgement within Discord's interaction response deadline.

## The first response is special

Use `interaction.response` for the initial acknowledgement. It can send a message, defer a response, edit the component message, or open a modal. Once the initial response is used, do not try to use it again for a second response; use `interaction.followup` or edit the original response as appropriate.

| Goal | Typical call |
|---|---|
| Reply privately | `interaction.response.send_message(..., ephemeral=True)` |
| Edit the message containing the component | `interaction.response.edit_message(...)` |
| Long-running operation | `interaction.response.defer(thinking=True, ephemeral=True)` then `interaction.followup.send(...)` |
| Update after deferred component message | defer in the correct mode, then edit the original response/message |
| Open a modal | `interaction.response.send_modal(MyModal())` |

The exact response mode depends on whether the interaction is a command or component. Read the [`InteractionResponse` API](https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.InteractionResponse) for details.

## Example: defer before network work

```python
async def refresh_status(self, interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True, thinking=True)
    try:
        status = await fetch_status_from_service()
    except TimeoutError:
        await interaction.followup.send("The status service timed out.", ephemeral=True)
        return
    await interaction.followup.send(f"Current status: {status}", ephemeral=True)
```

Do not perform long database or HTTP work before acknowledging the interaction. Use timeouts and handle expected failures.

## Editing the source message

When a button should update the existing panel, use `interaction.response.edit_message(view=...)` or edit the message with a fresh valid view. Keep in mind that the object you are editing may have become stale if other users changed the same shared state.

## Modal example

A modal is a separate interaction surface, not an item that is nested inside the V2 message layout. A button can open a modal as its initial response:

```python
class FeedbackModal(discord.ui.Modal, title="Send feedback"):
    feedback = discord.ui.TextInput(
        label="What should we improve?",
        style=discord.TextStyle.paragraph,
        max_length=1000,
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        value = str(self.feedback.value).strip()
        if not value:
            await interaction.response.send_message("Feedback cannot be empty.", ephemeral=True)
            return
        # Save feedback to your own store after validation.
        await interaction.response.send_message("Thanks, your feedback was received.", ephemeral=True)
```

```python
async def open_feedback(self, interaction: discord.Interaction):
    await interaction.response.send_modal(FeedbackModal())
```

Do not defer a button interaction and then try to open a modal as though it were still the initial response. Open the modal directly as the initial response. Newer `discord.py` releases introduce additional modal components; check your pinned version before using them.

## Ephemeral versus public responses

Ephemeral content is scoped to the invoking user and is appropriate for private selections, validations, and status feedback. Use public messages for shared updates the whole channel should see. Do not assume ephemeral responses can later be converted to public messages.

## Error paths

- If you catch an error, send a useful, non-sensitive response.
- Log technical details server-side; do not expose stack traces, tokens, or database URLs in Discord.
- If the interaction has already been acknowledged, use follow-up or edit methods rather than a second initial response.
- Keep callbacks short and delegate long-running tasks to services or background jobs.
