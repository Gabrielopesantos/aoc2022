from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def is_blocked(r: int, c: int, map: list[list[str]], max_y: int, dir: int = 0) -> bool:
    """
    dir - 0 = middle | -1 = left | 1 = right
    """

    return True if map[r+1][c+dir] == "#" or map[r+1][c+dir] == "o" else False


def compute(s: str) -> int:
    floor_size = 20000
    half_floor = floor_size // 2
    map = [["." for _ in range(floor_size)] for _ in range(600)]
    structs = s.splitlines()

    max_y = 0
    for struct_path in structs:
        path = [tuple(int(c) for c in reversed(point.split(",")))
                for point in struct_path.split(" -> ")]
        for i in range(len(path)-1):
            c_p, n_p = path[i], path[i+1]
            cp_x, cp_y = c_p
            np_x, np_y = n_p
            cp_y += half_floor
            np_y += half_floor
            max_y = max(max_y, cp_x, np_x)
            if cp_x == np_x:
                y_lower = min(cp_y, np_y)
                y_upper = max(cp_y, np_y)
                for y in range(y_lower, y_upper+1):
                    map[cp_x][y] = "#"
            elif cp_y == np_y:
                x_lower = min(cp_x, np_x)
                x_upper = max(cp_x, np_x)
                for x in range(x_lower, x_upper+1):
                    map[x][cp_y] = "#"

    for c in range(len(map[0])):
        map[max_y+2][c] = "#"

    sand = [(0, half_floor+500)]
    blocked = 0
    while True:
        if not sand:
            sand.append((0, half_floor+500))
        sand_r, sand_c = sand.pop()
        if is_blocked(sand_r, sand_c, map, max_y):
            if is_blocked(sand_r, sand_c, map, max_y, -1):
                if is_blocked(sand_r, sand_c, map, max_y, 1):
                    map[sand_r][sand_c] = "o"
                    blocked += 1
                    if sand_r == 0 and sand_c == half_floor+500:
                        break
                else:
                    sand_r += 1
                    sand_c += 1
                    sand.append((sand_r, sand_c))
            else:
                sand_r += 1
                sand_c -= 1
                sand.append((sand_r, sand_c))
        else:
            sand_r += 1
            sand.append((sand_r, sand_c))

    return blocked


INPUT_S = '''\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''
EXPECTED = 93


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
