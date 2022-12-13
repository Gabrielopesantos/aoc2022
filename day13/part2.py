from __future__ import annotations

import argparse
import json
from itertools import zip_longest
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def is_valid(l, r) -> int:
    l_type = type(l)
    r_type = type(r)

    if l_type == r_type and l_type == int:
        if l < r:
            return 1
        if l > r:
            return -1
        else:
            return 0
    if l_type == r_type and l_type == list:
        for l_v, r_v in zip_longest(l, r):
            if l_v is not None and r_v is None:
                return -1
            elif l_v is None and r_v is not None:
                return 1

            valid = is_valid(l_v, r_v)
            if valid != 0:
                return valid
    else:
        if l_type == int:
            l_lst = [l]
            return is_valid(l_lst, r)
        elif r_type == int:
            r_lst = [r]
            return is_valid(l, r_lst)


def validate_order(l, r) -> bool:
    correct_order = True
    for l_sig, r_sig in zip_longest(l, r):
        if l_sig is not None and r_sig is None:
            correct_order = False
            break
        elif l_sig is None and r_sig is not None:
            break

        valid = is_valid(l_sig, r_sig)
        if valid == 1:
            break
        elif valid == -1:
            correct_order = False
            break
        else:  # If 0
            continue

    return correct_order


def compute(s: str) -> int:
    packages = [pkg for pkg in s.strip().split(
        "\n") if pkg]
    packages.extend(["[[2]]", "[[6]]"])
    # Bubble sort
    for i in range(len(packages)):
        for j in range(i+1, len(packages)):
            left, right = json.loads(packages[i]), json.loads(packages[j])
            if not validate_order(left, right):
                packages[i], packages[j] = packages[j], packages[i]

    return (packages.index("[[2]]")+1) * (packages.index("[[6]]")+1)


INPUT_S = '''\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
'''
EXPECTED = 140


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
