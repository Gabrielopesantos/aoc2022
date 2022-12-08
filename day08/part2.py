from __future__ import annotations

import argparse
import os.path
import math

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    numbers = [[int(num) for num in line] for line in s.strip().split("\n")]
    rows, cols = len(numbers), len(numbers[0])
    scenic_scores = []

    def calc_scores(r, c):
        adj = ((1, 0), (0, 1), (-1, 0), (0, -1))
        trees = [0, 0, 0, 0]
        tree_val = numbers[r][c]
        for i, dir in enumerate(adj):
            score = 0
            adj_r, adj_c = r + dir[0], c + dir[1]
            while adj_r in range(rows) and adj_c in range(cols):
                score += 1
                if tree_val > numbers[adj_r][adj_c]:
                    adj_r += dir[0]
                    adj_c += dir[1]
                else:
                    break

            trees[i] = score

        return math.prod(trees)

    for r in range(rows):
        for c in range(cols):
            scenic_scores.append(calc_scores(r, c))

    return max(scenic_scores)


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 8


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
