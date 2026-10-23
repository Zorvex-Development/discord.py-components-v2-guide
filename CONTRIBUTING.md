# Contributing to the ZorveX Components V2 Handbook

Thank you for helping improve the guide. Contributions should make technical behaviour clearer and keep examples aligned with the supported `discord.py` API.

## Before opening a change

1. Check the official [discord.py stable documentation](https://discordpy.readthedocs.io/en/stable/) and cite the relevant page for version-sensitive claims.
2. Write explanations in your own words. Do not paste another tutorial verbatim.
3. Keep each guide focused; link to related sections instead of duplicating long explanations.
4. Use Python type hints when they improve clarity. Include imports in standalone examples.
5. Never add real bot tokens, application secrets, private user data, or private guild identifiers.

## Quality checks

- Syntax-check every standalone Python example with `python -m compileall examples`.
- For API-sensitive examples, run a smoke test with the documented `discord.py` version where practical.
- Check Markdown links and code fences.
- Explain any untested limitation instead of presenting assumptions as fact.

## Suggested commit style

- `docs: clarify LayoutView message restrictions`
- `fix: update select menu example`
- `examples: add persistent support panel`

## Licensing

By contributing, you confirm that you have the right to submit your contribution. The repository's license and contribution policy should be reviewed before merging changes. The custom license template is not legal advice and must have its publication placeholders completed.
