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
