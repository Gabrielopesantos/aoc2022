from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    overlaps = 0
    for line in lines:
        space_1, space_2 = [[int(s)
                             for s in s.split("-")] for s in line.strip().split(",")]
        space_1_rng = range(space_1[0], space_1[-1]+1)
        space_2_rng = range(space_2[0], space_2[-1]+1)

        if space_2[0] in space_1_rng or space_2[-1] in space_1_rng:
            overlaps += 1
        elif space_1[0] in space_2_rng or space_1[-1] in space_2_rng:
            overlaps += 1

    return overlaps


INPUT_S = '''\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''
EXPECTED = 4


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
