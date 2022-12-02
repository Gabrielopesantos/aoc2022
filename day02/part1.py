from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

POINTS_MAP = {
    "R": 1,
    "P": 2,
    "S": 3,
}

OPPONENT_MOVES = {
    "A": "R",
    "B": "P",
    "C": "S",
}

PLAYER_MOVES = {
        "X": "R",
        "Y": "P",
        "Z": "S",
    }

def compute(s: str) -> int:
    rounds = [lines.split(" ") for lines in s.splitlines()]
    player_points = 0
    for opp, player in rounds:
        opp_move, player_move = OPPONENT_MOVES[opp], PLAYER_MOVES[player]
        if opp_move == player_move:
            player_points += POINTS_MAP[player_move] + 3
        elif opp_move == "R" and player_move == "P":
            player_points += POINTS_MAP[player_move] + 6
        elif opp_move == "P" and player_move == "S":
            player_points += POINTS_MAP[player_move] + 6
        elif opp_move == "S" and player_move == "R":
            player_points += POINTS_MAP[player_move] + 6
        else:
            player_points += POINTS_MAP[player_move]
    return player_points


INPUT_S = '''\
A Y
B X
C Z
'''
EXPECTED = 15


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
