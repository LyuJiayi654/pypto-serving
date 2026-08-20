# Contributing

Keep changes scoped and document user-visible behavior with the code that
introduces it.

## Documentation

- Write external docs in user-facing language.
- Keep internal machine paths out of primary examples.
- Put model-specific constraints in the model page and support matrix.
- Update CLI, API, and configuration references when changing arguments or
  request fields.
- Prefer runnable commands with placeholders such as `/path/to/Qwen3-14B`.

## Code

- Follow Python 3.10 compatibility.
- Keep generated artifacts, caches, and compiled files out of commits.
- Add focused tests for scheduler, config, CLI, and profile behavior when those
  surfaces change.

## Skills

Repository-local agent skills live under `.agents/skills/`. Update
`.agents/skills/<skill-name>/SKILL.md` when changing a skill.
