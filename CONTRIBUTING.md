# Contributing

Contributions should improve prompt executability, continuity, or model stability without turning the skill into a visible template dump.

## Before Opening a Pull Request

1. Keep `SKILL.md` concise enough to act as the entry contract.
2. Put substantial reusable knowledge in `references/FILM_LANGUAGE_OPERATING_SYSTEM.md`.
3. Preserve Chinese-first visible output and short English technical terms only where they reduce ambiguity.
4. Keep Seedance segments independent, no longer than 15 seconds, and normally at least 5 seconds.
5. Do not submit private prompts, paid templates, cookies, tokens, copyrighted scripts, copied book passages, or exact film-scene reconstructions.
6. Add or update a source in `SOURCES.md` when a new rule depends on external research.

## Validation

Validate the skill with the Skill Creator validator when available:

```powershell
$env:PYTHONUTF8='1'
python quick_validate.py .
```

Also search the repository for credentials, local absolute paths, TODO markers, and encoding damage before committing.
