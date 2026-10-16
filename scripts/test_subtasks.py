#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from todotxt_subtask_sync import sync_subtask_lines


def apply(lines):
    out = list(lines)
    for line_no, new_line in sync_subtask_lines(out):
        out[line_no] = new_line
    return out


def test_parent_plus_marks_children():
    lines = [
        '+ Parent',
        '\tChild one',
        '\tChild two',
    ]
    result = apply(lines)
    assert result[1] == '\t+ Child one'
    assert result[2] == '\t+ Child two'


def test_parent_minus_marks_children_in_progress():
    lines = [
        '- Parent',
        '\tChild one',
        '\t+ Child was done',
    ]
    result = apply(lines)
    assert result[1] == '\t- Child one'
    assert result[2] == '\t- Child was done'


def test_parent_open_marks_children_in_progress():
    lines = [
        'Open parent',
        '\tChild',
    ]
    result = apply(lines)
    assert result[1] == '\t- Child'


def test_parent_changes_from_done_to_in_progress():
    lines = [
        '- Parent',
        '\t+ Child',
    ]
    result = apply(lines)
    assert result[1] == '\t- Child'


def main():
    test_parent_plus_marks_children()
    test_parent_minus_marks_children_in_progress()
    test_parent_open_marks_children_in_progress()
    test_parent_changes_from_done_to_in_progress()
    print('all subtask sync tests passed')


if __name__ == '__main__':
    main()
