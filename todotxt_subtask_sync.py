import re

STATE_MARKER_RE = re.compile(r'^(\+|-|\?|\*)\s')


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


def line_state_marker(content):
    if content.startswith('+ '):
        return '+'
    if content.startswith('- '):
        return '-'
    if content.startswith('? '):
        return '?'
    if content.startswith('* '):
        return '*'
    return None


def apply_state_prefix(content, desired_prefix):
    match = STATE_MARKER_RE.match(content)
    body = content[match.end():] if match else content
    return desired_prefix + body


def sync_subtask_lines(lines):
    stack = []
    replacements = []

    for line_no, line in enumerate(lines):
        level, content_start = line_indent_level(line)
        if line_is_comment_or_blank(line, content_start):
            continue

        content = line[content_start:]

        while stack and stack[-1][0] >= level:
            stack.pop()

        if stack and level > stack[-1][0]:
            parent_marker = stack[-1][1]
            desired = '+ ' if parent_marker == '+' else '- '
            new_content = apply_state_prefix(content, desired)
            if new_content != content:
                replacements.append((line_no, line[:content_start] + new_content))
                content = new_content

        stack.append((level, line_state_marker(content)))

    return replacements
