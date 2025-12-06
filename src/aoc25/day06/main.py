from curses import raw
from itertools import zip_longest
from pathlib import Path
import re

INPUT = Path(__file__).parent / "input"
# INPUT = Path(__file__).parent / "example"


def step1():
    data: list[list[str]] = [
        re.split(r" +", line.strip()) for line in INPUT.read_text().splitlines()
    ]
    total = 0
    for line in zip(*data):
        op = line[-1]
        operands = list(map(int, line[:-1]))
        if op == "+":
            total += sum(operands)
        elif op == "*":
            result = 1
            for n in operands:
                result *= n
            total += result
    print("Step 1:", total)


def step2():
    data: list[list[str]] = [
        re.split(r" +", line.strip()) for line in INPUT.read_text().splitlines()
    ]
    total = 0
    for line in zip(*data):
        op = line[-1]
        raw_numbers: list[str] = line[:-1]

        operands = [
            int("".join(n for n in nums if n is not None))
            for nums in zip_longest(*(reversed(n) for n in raw_numbers))
        ]
        if op == "+":
            total += sum(operands)
        elif op == "*":
            result = 1
            for n in operands:
                result *= n
            total += result
    print("Step 2:", total)


if __name__ == "__main__":
    step1()
    step2()
    # Attempt 1 - 9302499534581 - too low
