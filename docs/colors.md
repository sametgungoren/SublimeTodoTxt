# Optional * and ? colors (your theme)

This package does **not** override your color scheme or background. Syntax uses these scopes:

| Marker | Scope |
| --- | --- |
| `*` | `entity.task.todotxt.active` |
| `?` | `entity.task.todotxt.locked` |

To tint them green and purple, add rules to **your** color scheme (Preferences → Browse Color Schemes → open your theme → add):

```json
{
  "scope": "entity.task.todotxt.active",
  "foreground": "#22c55e"
},
{
  "scope": "entity.task.todotxt.locked",
  "foreground": "#a855f7"
}
```

Or copy optional `TodoTxt.sublime-color-scheme` rules into a User theme override without setting `"color_scheme"` in package settings.
