import re

import sublime
import sublime_plugin

VERSION = "v2026.10.16.11.45.36"

STATE_MARKER_RE = re.compile(r'^(\+|-|\?|\*)\s')
REGION_KEY = 'todotxt.subtask_inherited_done'
INHERITED_SCOPE = 'comment.line.todotxt.inherited'
BUSY_KEY = 'todotxt_subtask_busy'
STATUS_KEY = 'todotxt_version'


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


def line_indent_level(line):
    level = 0
    index = 0
    length = len(line)
    while index < length:
        char = line[index]
        if char == '\t':
            level += 1
            index += 1
            continue
        if char == ' ':
            end = index
            while end < length and line[end] == ' ':
                end += 1
            if end == index:
                break
            level += max(1, (end - index) // 4)
            index = end
            continue
        break
    return level, index


def line_is_comment_or_blank(line, content_start):
    body = line[content_start:].strip()
    return not body or body.startswith('//')


def analyze_subtasks(lines):
    stack = []
    inherited_lines = []
    prefix_inserts = []

    for line_no, line in enumerate(lines):
        level, content_start = line_indent_level(line)
        if line_is_comment_or_blank(line, content_start):
            continue

        content = line[content_start:]
        explicit_done = content.startswith('+ ')

        while stack and stack[-1][0] >= level:
            stack.pop()

        if stack and stack[-1][1] and level > stack[-1][0]:
            if not explicit_done:
                inherited_lines.append(line_no)
                if not STATE_MARKER_RE.match(content):
                    prefix_inserts.append((line_no, content_start))

        stack.append((level, explicit_done))

    return inherited_lines, prefix_inserts


def refresh_todotxt_view(view):
    if not is_todotxt_view(view):
        return
    TodoTxtSubtaskListener(view)._refresh()


def refresh_all_todotxt_views():
    for window in sublime.windows():
        for view in window.views():
            refresh_todotxt_view(view)


def plugin_loaded():
    sublime.set_timeout(refresh_all_todotxt_views, 0)


def plugin_unloaded():
    for window in sublime.windows():
        for view in window.views():
            view.erase_status(STATUS_KEY)
            view.erase_regions(REGION_KEY)


class TodoTxtSubtaskListener(sublime_plugin.ViewEventListener):
    def on_load(self):
        self._schedule()

    def on_activated(self):
        self._show_version()
        self._schedule()

    def on_modified(self):
        self._schedule()

    def _show_version(self):
        if is_todotxt_view(self.view):
            self.view.set_status(STATUS_KEY, f'TodoTxt {VERSION}')
        else:
            self.view.erase_status(STATUS_KEY)

    def _schedule(self):
        if not is_todotxt_view(self.view):
            return
        sublime.set_timeout(self._refresh, 50)

    def _refresh(self):
        if not is_todotxt_view(self.view):
            return
        if self.view.settings().get(BUSY_KEY):
            return

        inherit_color = self.view.settings().get('todotxt_subtask_inherit_done_color', True)
        auto_prefix = self.view.settings().get('todotxt_subtask_auto_prefix_done', True)

        lines = self.view.split_by_newlines()
        inherited_lines, prefix_inserts = analyze_subtasks(lines)

        if auto_prefix and prefix_inserts and not self.view.is_read_only():
            self.view.settings().set(BUSY_KEY, True)
            try:
                edit = self.view.begin_edit('todotxt_subtask_prefix')
                for line_no, content_start in reversed(prefix_inserts):
                    point = self.view.text_point(line_no, content_start)
                    self.view.insert(edit, point, '+ ')
                self.view.end_edit(edit)
                lines = self.view.split_by_newlines()
                inherited_lines, _ = analyze_subtasks(lines)
            finally:
                self.view.settings().erase(BUSY_KEY)

        if inherit_color:
            regions = []
            for line_no in inherited_lines:
                line = lines[line_no]
                level, content_start = line_indent_level(line)
                if line_is_comment_or_blank(line, content_start):
                    continue
                start = self.view.text_point(line_no, 0)
                end = self.view.text_point(line_no, len(line.rstrip('\n\r')))
                regions.append(sublime.Region(start, end))
            self.view.add_regions(
                REGION_KEY,
                regions,
                INHERITED_SCOPE,
                'dot',
                sublime.HIDDEN | sublime.PERSISTENT,
            )
        else:
            self.view.erase_regions(REGION_KEY)

        self._show_version()


class TodoTxtCompleteSubtasksCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        if not is_todotxt_view(view):
            sublime.error_message('TodoTxt: open a todo.txt file with the Todo.txt syntax first.')
            return

        lines = view.split_by_newlines()
        _, prefix_inserts = analyze_subtasks(lines)
        for line_no, content_start in reversed(prefix_inserts):
            point = view.text_point(line_no, content_start)
            view.insert(edit, point, '+ ')

        refresh_todotxt_view(view)


class TodoTxtRefreshCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        if view is None:
            return
        refresh_todotxt_view(view)
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
            f'If the version is old, reinstall from git and run '
            f'"Developer: Reload Window". Check the status bar for TodoTxt {VERSION}.'
        )
