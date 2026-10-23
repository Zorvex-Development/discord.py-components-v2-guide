# 18 — Modern modal components in discord.py 2.7

A modal is a separate interaction surface, not a child in a message's `LayoutView`. A V2 message can open a modal from a button or select callback, but the modal itself is submitted through the interaction response lifecycle.

## Version notes

- `discord.ui.Label` was introduced in `discord.py` 2.6 and provides a label/description wrapper around a modal input.
- `discord.ui.FileUpload`, `discord.ui.RadioGroup`, `discord.ui.Checkbox`, and `discord.ui.CheckboxGroup` were introduced in `discord.py` 2.7.
- These components are modal controls. Do not try to place `FileUpload` or modal-only radio/checkbox items inside a message `LayoutView`.
- Traditional `discord.ui.TextInput` remains useful. Read the [official modal API](https://discordpy.readthedocs.io/en/stable/interactions/api.html) for the currently supported constructor signatures.

## Modern text input with a label

```python
class FeedbackModal(discord.ui.Modal, title="Send feedback"):
    feedback = discord.ui.Label(
        text="What should we improve?",
        description="Please do not include passwords or private credentials.",
        component=discord.ui.TextInput(
            style=discord.TextStyle.paragraph,
            max_length=1000,
            required=True,
        ),
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        text_input = self.feedback.component
        value = str(text_input.value).strip()
        if not value:
            await interaction.response.send_message(
                "Feedback cannot be empty.", ephemeral=True
            )
            return
        # Validate and store the feedback through your application's service.
        await interaction.response.send_message(
            "Thanks, your feedback was received.", ephemeral=True
        )
```

## Radio group, checkbox, and file upload

This example demonstrates the 2.7 components. It deliberately does not download or store the uploaded file; production upload handling needs explicit size, MIME/type, filename, and storage controls.

```python
class RequestModal(discord.ui.Modal, title="Create a request"):
    summary = discord.ui.Label(
        text="Request summary",
        component=discord.ui.TextInput(max_length=500, required=True),
    )
    platform = discord.ui.Label(
        text="Target platform",
        component=discord.ui.RadioGroup(
            options=[
                discord.RadioGroupOption(label="Windows", value="windows"),
                discord.RadioGroupOption(label="Linux", value="linux"),
                discord.RadioGroupOption(label="macOS", value="macos"),
            ]
        ),
    )
    attachment = discord.ui.Label(
        text="Optional supporting file",
        description="Do not upload sensitive information.",
        component=discord.ui.FileUpload(required=False, min_values=0, max_values=1),
    )
    consent = discord.ui.Label(
        text="I have permission to share the attached file",
        component=discord.ui.Checkbox(default=False),
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        summary = str(self.summary.component.value).strip()
        platform = self.platform.component.value
        attachments = self.attachment.component.values
        has_consent = self.consent.component.value

        if not summary:
            await interaction.response.send_message(
                "A summary is required.", ephemeral=True
            )
            return
        if attachments and not has_consent:
            await interaction.response.send_message(
                "Confirm that you have permission to share the file.", ephemeral=True
            )
            return

        # In production: validate size/type, store safely, and persist the request.
        await interaction.response.send_message(
            f"Request received for **{platform}**. File count: {len(attachments)}.",
            ephemeral=True,
        )
```

Open it from the button interaction as the **initial response**:

```python
async def open_request_modal(self, interaction: discord.Interaction) -> None:
    await interaction.response.send_modal(RequestModal())
```

Do not defer the interaction before calling `send_modal()`. Modal opening is itself the initial response; if the interaction has already been acknowledged, a modal cannot be sent as a second initial response.

## Checkbox groups

When users may choose multiple labels, `discord.ui.CheckboxGroup` accepts `discord.CheckboxGroupOption` entries and exposes selected values. The group supports up to 10 options according to the current API reference. For a fixed single choice, a radio group is usually clearer.

## File upload safety checklist

1. Treat every uploaded file as untrusted input.
2. Enforce your own size and file-type policy before processing.
3. Do not trust the extension alone as proof of file type.
4. Use generated internal filenames rather than constructing a path from a user-supplied name.
5. Store files outside executable application directories and apply access controls.
6. Tell users what happens to their uploads and how long they are retained.

## Compatibility

These constructors rely on `discord.py` 2.7+. If a project deliberately pins 2.6, use the modal controls supported by that version or upgrade after testing. See [limits and compatibility](17-limits-and-compatibility.md) and the [official API reference](https://discordpy.readthedocs.io/en/stable/interactions/api.html).
