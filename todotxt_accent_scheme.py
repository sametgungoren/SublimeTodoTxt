import json
import os

ACCENT_FILENAME = 'TodoTxt-accent.sublime-color-scheme'
ACCENT_SCHEME = 'Packages/User/TodoTxt-accent.sublime-color-scheme'
META_FILENAME = '.todotxt_accent_meta.json'


def _user_dir(packages_path):
    return os.path.join(packages_path, 'User')


def _meta_path(packages_path):
    return os.path.join(_user_dir(packages_path), META_FILENAME)


def _accent_path(packages_path):
    return os.path.join(_user_dir(packages_path), ACCENT_FILENAME)


def _load_meta(packages_path):
    path = _meta_path(packages_path)
    try:
        with open(path, encoding='utf-8') as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return {}


def _save_meta(packages_path, meta):
    path = _meta_path(packages_path)
    with open(path, 'w', encoding='utf-8') as handle:
        json.dump(meta, handle, indent=2)
        handle.write('\n')


def resolve_base_color_scheme(preferences_get, packages_path):
    base = preferences_get('color_scheme', 'Mariana.sublime-color-scheme')
    if 'TodoTxt-accent' in base:
        stored = _load_meta(packages_path).get('base')
        if stored:
            return stored
    return base


def accent_colors_from_settings(settings_get):
    return {
        'active': settings_get('todotxt_accent_active_color', '#22c55e'),
        'locked': settings_get('todotxt_accent_locked_color', '#a855f7'),
    }


def build_accent_scheme_document(base_scheme, colors):
    return {
        'name': 'TodoTxt Accent',
        'extends': base_scheme,
        'variables': {
            'todotxt_active': colors['active'],
            'todotxt_locked': colors['locked'],
        },
        'rules': [
            {
                'scope': 'entity.task.todotxt.active',
                'foreground': 'var(todotxt_active)',
            },
            {
                'scope': 'entity.task.todotxt.active.marker',
                'foreground': 'var(todotxt_active)',
                'font_style': 'bold',
            },
            {
                'scope': 'entity.task.todotxt.locked',
                'foreground': 'var(todotxt_locked)',
            },
            {
                'scope': 'entity.task.todotxt.locked.marker',
                'foreground': 'var(todotxt_locked)',
                'font_style': 'bold',
            },
        ],
    }


def ensure_accent_color_scheme(packages_path, preferences_get, settings_get):
    if not settings_get('todotxt_accent_colors', True):
        return None

    base = resolve_base_color_scheme(preferences_get, packages_path)
    colors = accent_colors_from_settings(settings_get)
    meta = {'base': base, 'colors': colors}
    previous = _load_meta(packages_path)

    accent_path = _accent_path(packages_path)
    if previous == meta and os.path.isfile(accent_path):
        return ACCENT_SCHEME

    document = build_accent_scheme_document(base, colors)
    os.makedirs(_user_dir(packages_path), exist_ok=True)
    with open(accent_path, 'w', encoding='utf-8') as handle:
        json.dump(document, handle, indent=4)
        handle.write('\n')
    _save_meta(packages_path, meta)
    return ACCENT_SCHEME
