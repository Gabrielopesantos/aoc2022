"""
DOESN"T WORK - TOO SLOW
"""
from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def mahn_dist(x1, x2, y1, y2):
    return abs(x1-x2)+abs(y1-y2)


def compute(s: str) -> int:
    min_c = 0
    max_c = 4000000
    lines = s.splitlines()
    sensors = []
    beacons = []

    for line in lines:
        se_x, se_y, be_x, be_y = [int(num)
                                  for num in re.findall(r"-?\d+", line)]
        sensors.append((se_x, se_y))
        beacons.append((be_x, be_y))

    for x in range(min_c, max_c):
        for y in range(min_c, max_c):
            if all(True if mahn_dist(x, se_x, y, se_y) > mahn_dist(se_x, be_x, se_y, be_y) else
                    False for (se_x, se_y), (be_x, be_y) in zip(sensors, beacons)):
                return x * max_c + y


INPUT_S = '''\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''
EXPECTED = 56000011


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
