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


def compute(s: str) -> int:
    lines = [(line.split()[0], int(line.split()[-1]))
             for line in s.splitlines()]
    tail_pos = set()
    knots = [[0, 0] for _ in range(10)]
    for dir, steps in lines:
        while steps:
            dir_mot = DIRS[dir]
            knots[0][0] += dir_mot[0]
            knots[0][-1] += dir_mot[1]
            for k_i in range(1, len(knots)):
                x_diff = knots[k_i][0] - knots[k_i-1][0]
                y_diff = knots[k_i][-1] - knots[k_i-1][-1]
                if abs(x_diff) > 1 or abs(y_diff) > 1:
                    if x_diff == 0:
                        knots[k_i][-1] += -1 if y_diff > 0 else 1
                    elif y_diff == 0:
                        knots[k_i][0] += -1 if x_diff > 0 else 1
                    else:
                        knots[k_i][0] += -1 if x_diff > 0 else 1
                        knots[k_i][-1] += -1 if y_diff > 0 else 1
            tail_pos.add(tuple(knots[-1]))
            steps -= 1
    return len(tail_pos)


INPUT_ST_S = '''\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''

EXPECTED_ST = 1

INPUT_S = '''\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''
EXPECTED = 36


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
        (INPUT_ST_S, EXPECTED_ST),
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
