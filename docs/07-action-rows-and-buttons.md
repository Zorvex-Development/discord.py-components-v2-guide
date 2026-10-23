# 07 — ActionRow and buttons

`discord.ui.ActionRow` manually places interactive controls in a V2 layout. A row can contain up to five buttons or one select menu. Unlike a classic `discord.ui.View`, a `LayoutView` gives you more direct control over the whole message layout.

## Build a row with callbacks

```python
class ConfirmLayout(discord.ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=180)
        panel = discord.ui.Container()
        panel.add_item(discord.ui.TextDisplay("# Confirm action\nThis operation cannot be undone."))

        confirm = discord.ui.Button(
            label="Confirm", style=discord.ButtonStyle.success,
            custom_id="zorvex:confirm:yes"
        )
        cancel = discord.ui.Button(
            label="Cancel", style=discord.ButtonStyle.danger,
            custom_id="zorvex:confirm:no"
        )
        confirm.callback = self.confirm_action
        cancel.callback = self.cancel_action
        panel.add_item(discord.ui.ActionRow(confirm, cancel))
        self.add_item(panel)

    async def confirm_action(self, interaction: discord.Interaction):
        # Authorise the operation here before performing it.
        await interaction.response.send_message("Confirmation received.", ephemeral=True)

    async def cancel_action(self, interaction: discord.Interaction):
        await interaction.response.edit_message(view=None)
```

The callbacks above demonstrate the shape only. For a sensitive operation, validate the user, guild, target resource, and current state before confirming or cancelling anything.

## Button styles

- `discord.ButtonStyle.primary`: primary action.
- `discord.ButtonStyle.secondary`: neutral action.
- `discord.ButtonStyle.success`: positive/confirm action.
- `discord.ButtonStyle.danger`: destructive or cancel action.
- `discord.ButtonStyle.link`: navigates to a URL and does not dispatch a component callback.

Link buttons use `url="https://example.com"` and do not need a `custom_id`. Other interactive buttons need a stable `custom_id` if they must be persistent across restarts.

## Link button example

```python
link = discord.ui.Button(
    label="Documentation",
    style=discord.ButtonStyle.link,
    url="https://discordpy.readthedocs.io/en/stable/",
)
row = discord.ui.ActionRow(link)
panel.add_item(row)
```

## More than five controls

Create more rows instead of trying to fit extra buttons into one row:

```python
buttons = [
    discord.ui.Button(label=f"Option {index}", custom_id=f"option:{index}")
    for index in range(1, 8)
]
for offset in range(0, len(buttons), 5):
    panel.add_item(discord.ui.ActionRow(*buttons[offset:offset + 5]))
```

This constructs button items, but production code still needs callbacks assigned to each interactive button. A button with no callback is not a functioning feature.

## Dynamic callbacks

For dynamically created controls, assigning `button.callback = self.some_handler` is supported. Keep the handler signature as `async def handler(interaction: discord.Interaction)` and make sure each button is attached to the `LayoutView` before sending it.

## Interaction acknowledgement

A component interaction must be acknowledged. Use `interaction.response.send_message`, `edit_message`, `defer`, or `send_modal`, depending on what happens next. You can respond to an interaction only once using `interaction.response`; after that, use `interaction.followup` or edit the original response/message as appropriate.
