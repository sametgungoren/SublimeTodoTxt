# Installing in Sublime Text

Install either as an unpacked folder under **Packages** or as a `.sublime-package` archive.

## Method 1: Development folder (recommended)

Copy or symlink the full repository into Sublime’s **Packages** directory.

| Platform | Packages path |
| --- | --- |
| Linux | `~/.config/sublime-text/Packages/` |
| macOS | `~/Library/Application Support/Sublime Text/Packages/` |
| Windows | `%APPDATA%\Sublime Text\Packages\` |

Example (Linux):

```bash
ln -s /path/to/SublimeTodoTxt ~/.config/sublime-text/Packages/SublimeTodoTxt
```

Restart Sublime Text or run **Command Palette** → **Developer: Reload Window** after changes.

## Method 2: Package archive

```bash
./scripts/build-package.sh
```

Output: `dist/TodoTxt.sublime-package`

Copy it into **Installed Packages** (sibling of **Packages**):

| Platform | Installed Packages path |
| --- | --- |
| Linux | `~/.config/sublime-text/Installed Packages/` |
| macOS | `~/Library/Application Support/Sublime Text/Installed Packages/` |
| Windows | `%APPDATA%\Sublime Text\Installed Packages\` |

```bash
cp dist/TodoTxt.sublime-package ~/.config/sublime-text/Installed\ Packages/
```

## Syntax selection

Files named `todo.txt`, `done.txt`, or with extension `todotxt` use the **Todo.txt** syntax automatically.

Manual: **View** → **Syntax** → **Todo.txt**.

## State markers

Line prefixes (instead of standard `x`):

| Prefix | Meaning |
| --- | --- |
| `+` | Done |
| `-` | In progress |
| `?` | Locked |
| `*` | Active |

Inline project tags (`+Novel`) still require leading whitespace. A done line starts with `+ ` (plus then space).

## Verify the installed version

1. Open a `todo.txt` file with syntax **Todo.txt**.
2. Check the **status bar** (bottom right): `TodoTxt vYYYY.MM.DD.HH.MM.SS`.
3. **Command Palette** → **Todo.txt: Show Package Version**.

If the version is older than your git checkout or `plugin.py` on disk, Sublime is still loading another copy of the package.

### Common reasons updates do not appear

| Issue | What to do |
| --- | --- |
| Duplicate **Package Control** package `Todo.txt Syntax` | Remove it; keep only this fork under `Packages/SublimeTodoTxt` **or** `Installed Packages/TodoTxt.sublime-package`, not both. |
| Old `.sublime-package` in **Installed Packages** | Delete `TodoTxt.sublime-package`, copy the new file from `dist/`, reload window. |
| Symlink points to an old clone | `git pull` in the repo, then **Developer: Reload Window**. |
| Syntax not **Todo.txt** | **View** → **Syntax** → **Todo.txt** (plugin settings apply only with this syntax). |
| Buffer open before reload | **Todo.txt: Refresh Subtasks and Highlighting** or close and reopen the file. |

After `./scripts/build-package.sh`, the version string in `plugin.py` and the status bar updates to the build timestamp (UTC).
