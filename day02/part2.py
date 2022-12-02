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

GAME_OUTCOMES = {
    "X": "L",
    "Y": "D",
    "Z": "W",
}

def compute(s: str) -> int:
    rounds = [lines.split(" ") for lines in s.splitlines()]
    player_points = 0
    for opp, game in rounds:
        opp_move, game_outcome = OPPONENT_MOVES[opp], GAME_OUTCOMES[game]
        if game_outcome == "L":
            if opp_move == "R":
                player_points += POINTS_MAP["S"]
            elif opp_move == "P":
                player_points += POINTS_MAP["R"]
            else:
                player_points += POINTS_MAP["P"]
        elif game_outcome == "W":
            if opp_move == "R":
                player_points += POINTS_MAP["P"]
            elif opp_move == "P":
                player_points += POINTS_MAP["S"]
            else:
                player_points += POINTS_MAP["R"]
            player_points += 6
        else:
            player_points += POINTS_MAP[opp_move]
            player_points += 3
    return player_points


INPUT_S = '''\
A Y
B X
C Z
'''
EXPECTED = 12


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
