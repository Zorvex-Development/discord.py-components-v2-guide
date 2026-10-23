# 15 — Production patterns

This chapter combines the building blocks into an implementation approach suitable for bots that already have command, database, and service layers.

## Pattern A: separate layout builder from action logic

Keep the view responsible for rendering and interaction routing. Put ticket creation, billing, permissions, or database transactions in separate functions/services.

```python
class SupportPanel(discord.ui.LayoutView):
    def __init__(self, support_service):
        super().__init__(timeout=None)
        self.support_service = support_service
        panel = discord.ui.Container(accent_color=discord.Colour.blurple())
        panel.add_item(discord.ui.TextDisplay("# Support centre"))
        panel.add_item(discord.ui.TextDisplay("Choose the kind of help you need."))
        select = discord.ui.Select(
            placeholder="Select a topic",
            custom_id="zorvex:support:topic:v1",
            options=[
                discord.SelectOption(label="General help", value="general"),
                discord.SelectOption(label="Technical issue", value="technical"),
            ],
        )
        select.callback = self.choose_topic
        panel.add_item(discord.ui.ActionRow(select))
        self.add_item(panel)

    async def choose_topic(self, interaction: discord.Interaction):
        if interaction.guild is None:
            await interaction.response.send_message("Use this panel in a server.", ephemeral=True)
            return

        # In current discord.py, select components expose their values via the
        # relevant Select instance. A class-declared callback can reference that
        # instance directly; if routing from interaction.data, validate the raw value.
        data = interaction.data or {}
        values = data.get("values", [])
        allowed = {"general", "technical"}
        if len(values) != 1 or values[0] not in allowed:
            await interaction.response.send_message("Choose a valid topic.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True, thinking=True)
        try:
            ticket = await self.support_service.open_ticket(
                guild_id=interaction.guild.id,
                user_id=interaction.user.id,
                category=values[0],
            )
        except PermissionError:
            await interaction.followup.send("You cannot open a ticket here.", ephemeral=True)
            return
        except Exception:
            # Log the full error in production. Do not reveal internal details.
            await interaction.followup.send("The ticket could not be created. Please try again later.", ephemeral=True)
            return

        await interaction.followup.send(f"Ticket created: {ticket.reference}", ephemeral=True)
```

This is an integration pattern, not a complete ticket service: `support_service` must be implemented by your application, and your handler should log unexpected exceptions with a real logger. The selected category is allow-listed before it reaches the service.

## Pattern B: reusable panel factory

If a panel is mostly static, construct it in a function that accepts data and returns a `LayoutView`. This prevents command handlers from duplicating layout rules and allows snapshot-like tests of the expected content structure.

```python
def build_status_panel(title: str, details: list[str]) -> discord.ui.LayoutView:
    view = discord.ui.LayoutView(timeout=180)
    panel = discord.ui.Container(accent_color=discord.Colour.blurple())
    panel.add_item(discord.ui.TextDisplay(f"# {title}"))
    panel.add_item(discord.ui.Separator())
    for detail in details:
        panel.add_item(discord.ui.TextDisplay(detail))
    view.add_item(panel)
    return view
```

Before inserting dynamic text, validate and truncate it according to the application's input rules and total layout limits.

## Pattern C: pagination state

For a paginated result panel, keep the page index and result IDs in server-side state or in a short-lived view instance; do not trust the page number sent by a client. Clamp the index to the valid range, render only one page at a time, and disable Prev/Next at the boundaries. For long-lived dashboards, persist state and register the persistent view in `setup_hook`.

## Observability

For production interactions, log a correlation ID, command/action name, guild/message IDs where appropriate, duration, and failure category. Avoid logging tokens, full interaction payloads, or private text by default. Metrics worth tracking include interaction acknowledgement latency, callback errors, external service timeouts, and database conflict rate.

## Release checklist

- Test with the documented `discord.py` version.
- Confirm components render on mobile and desktop.
- Check callback permissions and race conditions.
- Confirm every callback acknowledges interactions.
- Test expired and deleted target resources.
- Keep API and dependency versions reproducible.
- Ensure `.env` and secrets are absent from the repository.
