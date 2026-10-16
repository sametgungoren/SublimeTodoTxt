import sublime
import sublime_plugin

from todotxt_accent_scheme import ensure_accent_color_scheme
from todotxt_subtask_sync import sync_subtask_lines

VERSION = "v2026.10.16.12.00.07"

STATUS_KEY = 'todotxt_version'
SYNC_BUSY_KEY = 'todotxt_sync_busy'


def is_todotxt_view(view):
    if view is None:
        return False
    syntax = (view.settings().get('syntax') or '').replace('\\', '/')
    if 'TodoTxt.sublime-syntax' in syntax:
        return True
    try:
        if view.size() == 0:
            return view.match_selector(0, 'text.todotxt')
        for region in view.sel():
            if view.match_selector(region.begin(), 'text.todotxt'):
                return True
    except (ValueError, IndexError):
        pass
    return view.match_selector(0, 'text.todotxt')


def apply_todotxt_accent(view):
    if not is_todotxt_view(view):
        return

    settings_get = view.settings().get
    if not settings_get('todotxt_accent_colors', True):
        view.settings().erase('color_scheme')
        return

    scheme = ensure_accent_color_scheme(
        sublime.packages_path(),
        sublime.load_settings('Preferences.sublime-settings').get,
        settings_get,
    )
    if scheme:
        view.settings().set('color_scheme', scheme)


def schedule_sync(view):
    if not is_todotxt_view(view):
        return
    sublime.set_timeout(lambda: view.run_command('todotxt_sync_subtasks'), 50)


def refresh_all_todotxt_views():
    for window in sublime.windows():
        for view in window.views():
            if is_todotxt_view(view):
                apply_todotxt_accent(view)
                schedule_sync(view)


def plugin_loaded():
    sublime.set_timeout(refresh_all_todotxt_views, 0)


def plugin_unloaded():
    for window in sublime.windows():
        for view in window.views():
            view.erase_status(STATUS_KEY)


class TodoTxtSettingsListener(sublime_plugin.EventListener):
    def on_settings_changed(self, settings):
        if settings.get('color_scheme') is None:
            return
        name = settings.get('default_name', '')
        if name != 'Preferences.sublime-settings':
            return
        sublime.set_timeout(refresh_all_todotxt_views, 0)


class TodoTxtSubtaskListener(sublime_plugin.ViewEventListener):
    def on_load(self):
        apply_todotxt_accent(self.view)
        schedule_sync(self.view)

    def on_activated(self):
        if is_todotxt_view(self.view):
            self.view.set_status(STATUS_KEY, f'TodoTxt {VERSION}')
            apply_todotxt_accent(self.view)
        else:
            self.view.erase_status(STATUS_KEY)
        schedule_sync(self.view)

    def on_modified(self):
        if self.view.settings().get(SYNC_BUSY_KEY):
            return
        schedule_sync(self.view)


class TodoTxtSyncSubtasksCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        if not is_todotxt_view(view):
            return
        if not view.settings().get('todotxt_sync_subtasks', True):
            return
        if view.is_read_only():
            return

        lines = view.split_by_newlines()
        replacements = sync_subtask_lines(lines)
        if not replacements:
            return

        view.settings().set(SYNC_BUSY_KEY, True)
        try:
            for line_no, new_line in reversed(replacements):
                line = lines[line_no]
                start = view.text_point(line_no, 0)
                end = view.text_point(line_no, len(line))
                view.replace(edit, sublime.Region(start, end), new_line)
        finally:
            view.settings().erase(SYNC_BUSY_KEY)

        if is_todotxt_view(view):
            view.set_status(STATUS_KEY, f'TodoTxt {VERSION}')


class TodoTxtCompleteSubtasksCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('todotxt_sync_subtasks')


class TodoTxtRefreshCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        if view is None:
            return
        apply_todotxt_accent(view)
        view.run_command('todotxt_sync_subtasks')
        sublime.status_message(f'TodoTxt {VERSION}: refreshed')


class TodoTxtShowVersionCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        view = sublime.active_window().active_view() if sublime.active_window() else None
        in_todo = is_todotxt_view(view) if view else False
        syntax = view.settings().get('syntax') if view else '(no view)'
        sublime.message_dialog(
            f'TodoTxt package version: {VERSION}\n\n'
            f'Active view is todo syntax: {in_todo}\n'
            f'Syntax path: {syntax}\n\n'
            f'Subtasks sync when the parent line uses + (children get +) or any '
            f'other state (children get -). Triggered on edit, open, and reload.'
        )
