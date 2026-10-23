# 08 — Select menus

Select menus let a user make a bounded choice. In Components V2 they are placed in an `ActionRow`. A row may contain one select menu, not a menu and additional buttons together.

## Menu types

| Class | Selection |
|---|---|
| `discord.ui.Select` | A predefined list of string options |
| `discord.ui.UserSelect` | User or member targets |
| `discord.ui.RoleSelect` | Server roles |
| `discord.ui.ChannelSelect` | Channels, optionally filtered by channel type |
| `discord.ui.MentionableSelect` | Users and roles |

Availability and argument details can vary by library version. Check the [Select Menus API](https://discordpy.readthedocs.io/en/stable/interactions/api.html#select-menus).

## String select example

```python
class CategoryLayout(discord.ui.LayoutView):
    def __init__(self):
        super().__init__(timeout=180)
        panel = discord.ui.Container()
        panel.add_item(discord.ui.TextDisplay("# Support\nChoose the type of request."))

        menu = discord.ui.Select(
            placeholder="Choose a category…",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(label="General", value="general", description="General questions"),
                discord.SelectOption(label="Billing", value="billing", description="Payment and invoices"),
                discord.SelectOption(label="Technical", value="technical", description="Something is not working"),
            ],
            custom_id="zorvex:support:category",
        )
        self.category_menu = menu
        menu.callback = self.category_selected
        panel.add_item(discord.ui.ActionRow(menu))
        self.add_item(panel)

    async def category_selected(self, interaction: discord.Interaction):
        selected = self.category_menu.values
        # Values are still user input; validate them against known allowed values.
        allowed = {"general", "billing", "technical"}
        if len(selected) != 1 or selected[0] not in allowed:
            await interaction.response.send_message("That selection is not valid.", ephemeral=True)
            return
        await interaction.response.send_message(f"Selected: **{selected[0]}**", ephemeral=True)
```

The callback above reads the selected values from the retained `Select` instance, using the public `.values` property. Validate those values against an allow-list even though the options were originally created by your own code.

## Entity select menus

Entity selects return Discord entities or resolved data rather than arbitrary strings. For example, a role-selection panel can be built as:

```python
role_select = discord.ui.RoleSelect(
    placeholder="Choose a role",
    min_values=1,
    max_values=1,
    custom_id="zorvex:settings:role",
)
role_select.callback = self.role_selected
panel.add_item(discord.ui.ActionRow(role_select))
```

Inside the handler, inspect the selected roles and verify that the invoking user is allowed to manage the chosen target. Never grant a role just because it appeared in a submitted select interaction.

## Option limits and UX

A string select supports a limited number of options (Discord's documented maximum is 25). If the list is larger, group choices, paginate through buttons, or ask the user to narrow the selection first. Give options distinct labels and values. Keep values stable for routing and labels human-readable.

## Security checklist

- Validate submitted values on the server.
- Verify actor permissions and target scope.
- Consider whether the menu should work in DMs, guilds, or both.
- Respond to every interaction promptly.
- Treat a menu as input, not as proof that the user is authorised.
