# Publish To GitHub

Remote configured for this release:

```bash
git remote -v
```

Expected remote:

```text
origin  https://github.com/Chenghaoj/computational-structural-biology-platform.git
```

Publish commands:

```bash
git status
git add .
git commit -m "Initial public release of computational structural biology platform"
git push
```

Do not push if `FINAL_RELEASE_AUDIT.md` reports unresolved `PRIVATE_REMOVE_BEFORE_UPLOAD` items.
