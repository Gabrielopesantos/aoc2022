from __future__ import annotations

import argparse
import os.path
from typing import Optional

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Dir:
    def __init__(self, name: str, parent: Optional[Dir] = None, size: int = 0):
        self.parent = None
        self.children = {}
        self.name = name
        self.size = size


above_th = []


def inorder(node):
    if not node.children:
        if node.size <= 100000:
            above_th.append((node.name, node.size))
        return node.size

    size = 0
    for ch in node.children.values():
        size += inorder(ch)

    node.size += size
    if node.size <= 100000:
        above_th.append((node.name, node.size))

    return node.size


def compute(s: str) -> int:
    commands = s.split("\n")[1:]
    curr_com = 0
    node = Dir(name="/")
    while curr_com <= len(commands)-1:
        comm_f, *comm_r = commands[curr_com].split(" ")
        if comm_f == "$":
            op = comm_r[0]
            if op == "ls":
                dir_size = 0
                curr_com += 1
                inner_comm_f, *inner_comm_r = commands[curr_com].split(" ")
                while inner_comm_f == "dir" or inner_comm_f.isdigit():
                    if inner_comm_f == "dir":
                        dir_name = inner_comm_r[0]
                        dir = Dir(name=dir_name)
                        node.children[dir_name] = dir
                    elif inner_comm_f.isdigit():
                        dir_size += int(inner_comm_f)
                    else:
                        break

                    curr_com += 1
                    inner_comm_f, *inner_comm_r = commands[curr_com].split(" ")

                curr_com -= 1
                node.size = dir_size

            elif op == "cd":
                cd_loc = comm_r[-1]
                if cd_loc == "..":
                    parent = node.parent
                    node = parent
                else:
                    child = node.children[cd_loc]
                    child.parent = node
                    node = child

        curr_com += 1

    while node.name != "/":
        parent = node.parent
        node = parent

    node.size = inorder(node)

    return sum(size for n, size in above_th)


INPUT_S = '''\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''
EXPECTED = 95437


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
