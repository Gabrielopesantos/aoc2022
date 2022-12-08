from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    numbers = [[int(num) for num in line] for line in s.strip().split("\n")]
    rows, cols = len(numbers), len(numbers[0])
    visible = set()

    """
    (0, 0)    (0, -1)
    ----------
    |        |
    |        |
    |        |
    |        |
    ----------
    (-1, 0)   (-1, -1)
    """
    for r in range(rows):
        col = 0
        visible.add((r, col, numbers[r][col]))
        col_mx = numbers[r][col]
        while col in range(cols-2):
            if numbers[r][col+1] > numbers[r][col] and numbers[r][col+1] > col_mx:
                visible.add((r, col+1, numbers[r][col+1]))
                col_mx = max(col_mx, numbers[r][col+1])
            col += 1

        col_rev = cols-1
        visible.add((r, col_rev, numbers[r][col_rev]))
        col_rev_mx = numbers[r][col_rev]
        while col_rev in range(2, cols):
            if numbers[r][col_rev-1] > numbers[r][col_rev] and numbers[r][col_rev-1] > col_rev_mx:
                visible.add((r, col_rev-1, numbers[r][col_rev-1]))
                col_rev_mx = max(col_rev_mx, numbers[r][col_rev-1])
            col_rev -= 1

    for c in range(cols):
        row = 0
        visible.add((row, c, numbers[row][c]))
        row_mx = numbers[row][c]
        while row in range(rows-2):
            if numbers[row+1][c] > numbers[row][c] and numbers[row+1][c] > row_mx:
                visible.add((row+1, c, numbers[row+1][c]))
                row_mx = max(row_mx, numbers[row+1][c])
            row += 1

        row_rev = rows-1
        visible.add((row_rev, c, numbers[row_rev][c]))
        row_rev_mx = numbers[row_rev][c]
        while row_rev in range(2, rows):
            if numbers[row_rev-1][c] > numbers[row_rev][c] and numbers[row_rev-1][c] > row_rev_mx:
                visible.add((row_rev-1, c, numbers[row_rev-1][c]))
                row_rev_mx = max(row_rev_mx, numbers[row_rev-1][c])
            row_rev -= 1

    return len(visible)


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 21


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
