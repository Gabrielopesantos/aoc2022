from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Monkey:
    def __init__(self, id: int, items: list[int], operation: str, test: tuple[int, int, int]):
        self.id = id
        self.items: list[int] = []
        self.items.extend(items)
        self.op = operation
        self.test = test
        self.inspects: int = 0

    def calc_updated_worrying_lvl(self, old: str) -> int:
        op = self.op
        equation_op = op.replace("old", old)
        return eval(equation_op)  # eval


def compute(s: str) -> int:
    monkeys_str = s.split("\n\n")
    monkeys = {}
    for m_str in monkeys_str:
        m_split_strs = m_str.split("\n")
        monkey_id = int(m_split_strs[0][m_split_strs[0].index(":")-1])
        monkey_items = tuple(int(s.strip(" ,"))
                             for s in m_split_strs[1].split() if s.strip(" ,").isdigit())
        monkey_op = m_split_strs[2][m_split_strs[2].index("=")+1:].strip()
        divisible = tuple(int(s)
                          for s in m_split_strs[3].split() if s.isdigit())[0]
        true_ = int(m_split_strs[4][-1])
        false_ = int(m_split_strs[5][-1])
        monkey_test = (divisible, true_, false_)

        monkey = Monkey(monkey_id, monkey_items, monkey_op, monkey_test)
        monkeys[monkey_id] = monkey

    rounds: int = 20
    while rounds:
        for monkey in monkeys.values():
            while monkey.items:
                itm = monkey.items.pop()
                item_worrying_lvl = monkey.calc_updated_worrying_lvl(str(itm))
                bored_worrying_lvl = item_worrying_lvl // 3
                divisible_val, true_monkey, false_monkey = monkey.test
                if bored_worrying_lvl % divisible_val == 0:
                    monkeys[true_monkey].items.append(bored_worrying_lvl)
                else:
                    monkeys[false_monkey].items.append(bored_worrying_lvl)

                monkey.inspects += 1

        rounds -= 1

    inspections = sorted((m.inspects for m in monkeys.values()))
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
EXPECTED = 10605


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
