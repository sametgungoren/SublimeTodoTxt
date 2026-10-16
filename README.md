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
