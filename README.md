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

Syntax scopes alone do not set colors; this package ships `TodoTxt.sublime-color-scheme` (extends built-in Mariana) for todo buffers:

| State | Scope | Foreground |
| --- | --- | --- |
| Active `*` | `entity.task.todotxt.active` | `#22c55e` (green) |
| Locked `?` | `entity.task.todotxt.locked` | `#a855f7` (purple) |

To keep your global theme, remove or override `color_scheme` in **User** `TodoTxt.sublime-settings` and add the same scope rules to your color scheme.

### Subtasks (indented lines)

Child lines use one or more leading tabs (or 4-space steps) under a parent task. If the parent line is completed (`+ ` at that indent level), then:

- Subtasks without `+` are styled as done (`comment.line.todotxt.inherited`).
- With `todotxt_subtask_auto_prefix_done` (default **true**), `+ ` is inserted at the start of each affected subtask line that has no state marker (`+`, `-`, `?`, `*`).

Example:

```
+ Postgre refactoring
	NotificationService is done
	+ OptimoveBatchData is done
```

After refresh, the second line becomes `\t+ NotificationService is done` and all lines use done styling.

Settings in `TodoTxt.sublime-settings`:

- `todotxt_subtask_inherit_done_color` (default `true`)
- `todotxt_subtask_auto_prefix_done` (default `true`; set `false` to only color, not edit)

Command palette: **Todo.txt: Prefix + on Subtasks Under Completed Parents**.

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
