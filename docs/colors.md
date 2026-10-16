# Active (*) and locked (?) colors

Todo buffers use **accent colors only**: the plugin writes `Packages/User/TodoTxt-accent.sublime-color-scheme`, which **extends your current global color scheme** (Preferences → color scheme). Background and all other scopes stay on your theme; only these scopes get extra foreground rules:

| Marker | Scope | Default |
| --- | --- | --- |
| `*` | `entity.task.todotxt.active` | `#22c55e` |
| `?` | `entity.task.todotxt.locked` | `#a855f7` |

Settings in `Todo.txt.sublime-settings` (or User override):

```json
{
  "todotxt_accent_colors": true,
  "todotxt_accent_active_color": "#22c55e",
  "todotxt_accent_locked_color": "#a855f7"
}
```

Set `todotxt_accent_colors` to `false` to use only your theme with no todo-specific scheme file.

When you change the global theme, the accent file is regenerated on the next todo view activation.
