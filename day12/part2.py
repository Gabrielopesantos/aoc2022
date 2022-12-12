from __future__ import annotations

import argparse
import os.path
import string

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    heights_map = {ch: val for val, ch in enumerate(string.ascii_lowercase)}
    heights_map["S"] = heights_map["a"]
    heights_map["E"] = heights_map["z"]
    map = [list(line) for line in s.splitlines()]
    rows, cols = len(map), len(map[0])
    adj = ((0, 1), (1, 0), (0, -1), (-1, 0))
    path_steps = []

    def bfs(r, c):
        n_steps = []
        seen = set()
        seen.add((r, c))
        path_stack = [(r, c, 0)]
        while path_stack:
            for _ in range(len(path_stack)):
                r, c, steps = path_stack.pop(0)

                if n_steps and steps > sorted(n_steps)[0]:
                    # If curr_path is already higher then the current best, skip
                    continue

                if map[r][c] == "E":
                    n_steps.append(steps)
                    continue

                for del_r, del_c in adj:
                    adj_r, adj_c = r + del_r, c + del_c
                    if (adj_r in range(rows) and adj_c in range(cols) and (adj_r, adj_c) not in seen
                            and heights_map["a"] <= heights_map[map[adj_r][adj_c]] <= heights_map[map[r][c]] + 1):
                        seen.add((adj_r, adj_c))
                        path_stack.append((adj_r, adj_c, steps+1))
        return n_steps

    for r in range(rows):
        for c in range(cols):
            if map[r][c] == "a" or map[r][c] == "S":
                path_steps.extend(bfs(r, c))

    return sorted(path_steps)[0]


INPUT_S = '''\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''
EXPECTED = 29


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
