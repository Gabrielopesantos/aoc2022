from __future__ import annotations

import argparse
import os.path
import string

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

CHARS_MAP = string.ascii_lowercase + string.ascii_uppercase


def compute(s: str) -> int:
    priority_sum = 0
    lines = s.splitlines()
    group = 1
    rucksacks = []
    for line in lines:
        rucksacks.append(set(line))
        if group == 3:
            badge = (rucksacks[0] & rucksacks[1] & rucksacks[2]).pop()
            badge_priority = CHARS_MAP.index(badge) + 1
            priority_sum += badge_priority

            group = 0
            rucksacks.clear()

        group += 1

    return priority_sum


INPUT_S = '''\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''
EXPECTED = 70


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
