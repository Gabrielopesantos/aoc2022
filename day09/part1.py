from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

DIRS = {
    "R": (0, -1),
    "U": (-1, 0),
    "L": (0, 1),
    "D": (1, 0),
}


def coords_dist(x1, x2, y1, y2):
    return abs(x1-x2) + abs(y1-y2)


def compute(s: str) -> int:
    lines = [(line.split()[0], int(line.split()[-1]))
             for line in s.splitlines()]
    tail_pos = set()
    head = [0, 0]
    tail = [0, 0]
    for dir, steps in lines:
        while steps:
            dir_mot = DIRS[dir]
            head[0] += dir_mot[0]
            head[1] += dir_mot[1]
            dist = coords_dist(head[0], tail[0], head[-1], tail[-1])
            if dist == 2:
                if head[0] == tail[0]:
                    tail[-1] += dir_mot[-1]
                elif head[-1] == tail[-1]:
                    tail[0] += dir_mot[0]
            elif dist > 2:
                tail[0] = head[0] - dir_mot[0]
                tail[-1] = head[-1] - dir_mot[-1]
            tail_pos.add(tuple(tail))
            steps -= 1
    return len(tail_pos)


INPUT_S = '''\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''
EXPECTED = 13


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
