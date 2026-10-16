# SublimeTodoTxt

Syntax highlighting and `@` / `+` autocompletion for [Todo.txt](http://todotxt.com) task lists in [Sublime Text](http://www.sublimetext.com) (Sublime Text 3 and 4).

![Screenshot](Screenshot.png)

## Task states

This fork uses line-prefix markers instead of the standard Todo.txt `x` completion marker:

| Prefix | State |
| --- | --- |
| `+` | Done |
| `-` | In progress |
| `?` | Locked |
| `*` | Active (current focus) |

Example:

```
(A) Call Mom @Phone +Family
- Outline chapter 5 +Novel @Computer
? Waiting on publisher reply +Novel
* Research self-publishing services +Novel @Computer
+ Download Todo.txt mobile app @Phone
```

Priorities `(A)`–`(Z)`, `@context`, inline `+project`, dates, and `//` comments behave as before. Project tags such as `+Novel` stay in the line body; a completed task starts with `+ ` (plus and a space).

### Colors

The package does **not** change your color scheme or background. `*` and `?` use scopes `entity.task.todotxt.active` and `entity.task.todotxt.locked`; your theme controls the colors. Optional green/purple: [docs/colors.md](docs/colors.md).

### Subtasks (indented lines)

Child lines use leading tabs (or 4-space steps). **Immediate parent** drives status (sync runs on edit, open, reload):

| Parent prefix | Child lines become |
| --- | --- |
| `+ ` (done) | `+ ` |
| anything else (`-`, `?`, `*`, or open) | `- ` |

Example after sync:

```
+ Postgre refactoring
	+ NotificationService is done
	+ OptimoveBatchData is done
```

Change parent to `- Postgre refactoring` and children revert to `- …`.

Setting: `todotxt_sync_subtasks` (default `true`). Command palette: **Todo.txt: Sync Subtask Status From Parent**.

## Version

Each `./scripts/build-package.sh` run sets `VERSION` in `plugin.py` to `vUTC-YYYY.MM.DD.HH.MM.SS`. With a todo file focused, the status bar shows `TodoTxt <version>`. Use **Todo.txt: Show Package Version** to confirm Sublime loaded this package and not Package Control’s upstream syntax-only build.

## Installation

See [docs/installation.md](docs/installation.md) for platform paths and details.

### Build package

```bash
chmod +x scripts/build-package.sh
./scripts/build-package.sh
```

Copy `dist/TodoTxt.sublime-package` into Sublime’s **Installed Packages** directory.

### Development

Symlink or copy this repository under `Packages/SublimeTodoTxt`, then **Developer: Reload Window** after syntax changes.

### Package Control

The upstream [Todo.txt Syntax](https://packagecontrol.io/packages/Todo.txt%20Syntax) package uses standard `x` semantics; use manual install for this fork.

## Settings

Optional auto-save on focus loss in your **User** package (`TodoTxt.sublime-settings`):

```json
{
   "save_on_focus_lost": true
}
```

The package suggests existing `@context` and `+project` tokens from the file (`TodoTxt.sublime-settings`).

## Credits

Based on the original SublimeTodoTxt / Package Control project; this repository adds custom state markers.
