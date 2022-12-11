"""
DOES NOT WORK
"""
from __future__ import annotations

import argparse
import os.path
import math

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Monkey:
    def __init__(self, id: int, items: list[Item], operation: tuple[str, str, str], test: tuple[int, int, int]):
        self.id = id
        self.items: list[Item] = []
        self.items.extend(items)
        self.op = operation
        self.test = test
        self.inspects: int = 0

    def calc_updated_worrying_lvl(self, old: int) -> int:
        val = 0
        operand1 = old if self.op[0] == "old" else int(self.op[0])
        operand2 = old if self.op[2] == "old" else int(self.op[2])
        if self.op[1] == "+":
            val = operand1 + operand2
        elif self.op[1] == "*":
            val = operand1 * operand2

        return val


class Item:
    def __init__(self, worrying_lvl: int):
        self.worrying_lvl = worrying_lvl
        self.divisors = []


def compute(s: str) -> int:
    monkeys_str = s.split("\n\n")
    monkeys = {}
    for m_str in monkeys_str:
        m_split_strs = m_str.split("\n")
        monkey_id = int(m_split_strs[0][m_split_strs[0].index(":")-1])
        monkey_items = tuple(Item(int(s.strip(" ,")))
                             for s in m_split_strs[1].split() if s.strip(" ,").isdigit())
        monkey_op = m_split_strs[2][m_split_strs[2].index(
            "=")+1:].strip().split()
        divisor = tuple(int(s)
                        for s in m_split_strs[3].split() if s.isdigit())[0]
        true_ = int(m_split_strs[4][-1])
        false_ = int(m_split_strs[5][-1])
        monkey_test = (divisor, true_, false_)

        monkey: dict(int, Monkey) = Monkey(
            monkey_id, monkey_items, monkey_op, monkey_test)
        monkeys[monkey_id] = monkey

    rounds: int = 20
    while rounds:
        for monkey in monkeys.values():
            divisor, true_monkey, false_monkey = monkey.test
            while monkey.items:
                itm = monkey.items.pop()
                itm.divisors.append(divisor)
                item_worrying_lvl = monkey.calc_updated_worrying_lvl(
                    itm.worrying_lvl)
                worrying_lvl_rem = item_worrying_lvl % math.prod(itm.divisors)
                print(
                    f"{worrying_lvl_rem=} {item_worrying_lvl=} {math.prod(itm.divisors)=} ({len(itm.divisors)})")
                new_itm = Item(item_worrying_lvl)
                new_itm.divisors.extend(itm.divisors)
                if worrying_lvl_rem == 0:
                    monkeys[true_monkey].items.append(new_itm)
                else:
                    monkeys[false_monkey].items.append(new_itm)

                monkey.inspects += 1

        if rounds in (20, 1):
            print(rounds, [(m.id, m.inspects)
                  for m in monkeys.values()])
        rounds -= 1

    inspections = sorted((m.inspects for m in monkeys.values()))
    # print(inspections)
    return inspections[-1] * inspections[-2]


INPUT_S = '''\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''
EXPECTED = 2713310158


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
