from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    puzzle, moves = s.split("\n\n")
    rev_puzzle = [list(reversed(line)) for line in puzzle[::-1].split("\n")]
    puzzle_stacks = []
    str_pos = 0
    # Scuffed
    while True:
        try:
            is_digit = rev_puzzle[0][str_pos].isdigit()
        except Exception:
            break
        else:
            if is_digit:
                pos_stack = []
                col_pos = 1
                while True:
                    try:
                        char = rev_puzzle[col_pos][str_pos]
                    except IndexError:
                        break
                    if char != " ":
                        pos_stack.append(rev_puzzle[col_pos][str_pos])
                    col_pos += 1
                puzzle_stacks.append(pos_stack)
            str_pos += 1

    for move in moves.strip().split("\n"):
        n, frm, to = [int(s) for s in move.split() if s.isdigit()]
        frm, to = frm - 1, to - 1
        while n and puzzle_stacks[frm]:
            crate = puzzle_stacks[frm].pop()
            puzzle_stacks[to].append(crate)
            n -= 1
    top_crates = ""
    for stack in puzzle_stacks:
        top_crates += stack[-1]

    return top_crates  # Doesn't work with aoc-submit --part 1


INPUT_S = '''\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''
EXPECTED = "CMZ"


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
