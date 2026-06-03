# Translation Policy

English (current)

This repository supports bilingual documentation in English and Simplified Chinese.

## Source of Truth

English documents are the canonical source. Simplified Chinese documents are translations and should follow the English structure as closely as practical.

## Translation Rules

- Commands must remain identical.
- File paths must remain identical.
- Script names must remain identical.
- Module names must remain identical.
- Software names must remain identical.
- Technical examples must remain synchronized.
- Only explanatory text should be translated.

## Code Blocks

Do not machine-translate code blocks. Code blocks in translated documents should be copied from the canonical English document unless the block is prose-only and intentionally localized.

## Language Switchers

Every bilingual document should start with a language switcher:

```text
English (current) | [Simplified Chinese link]
```

```text
[English link] | 简体中文（当前）
```

## Synchronization

Update `docs/translation_status.md` whenever English or Chinese documentation changes. If the English source changes and the Chinese translation is not updated in the same pull request, mark the row as `needs_sync`.

## Review

Translation review should check meaning, command preservation, link validity, and consistency of technical terms. When in doubt, preserve the English technical term.
