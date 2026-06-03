# Translation Policy

English (current)

This repository supports bilingual documentation in English and Simplified Chinese.

## Source of Truth

English documents are the canonical source. Simplified Chinese documents are translations and should follow the English structure as closely as practical.

## Homepage Language Switching

The GitHub homepage uses centered language switchers at the top of both README files:

```html
<p align="center">
  🇺🇸 English | 🇨🇳 [简体中文](../README.zh-CN.md)
</p>
```

```html
<p align="center">
  🇺🇸 [English](../README.md) | 🇨🇳 简体中文
</p>
```

## Translation Rules

- Commands must remain identical.
- File paths must remain identical.
- Script names must remain identical.
- Module names must remain identical.
- Software names must remain identical.
- Technical examples must remain synchronized.
- Only explanatory text should be translated.

## Code Blocks

Do not translate command blocks or code blocks. Code blocks in translated documents should be copied from the canonical English document unless the block is prose-only and intentionally localized.

## Synchronization

Update `docs/translation_status.md` whenever English or Chinese documentation changes. If the English source changes and the Chinese translation is not updated in the same pull request, mark the row as `needs_sync`.

## Review

Translation review should check meaning, command preservation, link validity, GitHub rendering, and consistency of technical terms. When in doubt, preserve the English technical term.
