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
    data: list[str] = INPUT.read_text().splitlines(keepends=True)
    total = 0
    last_op = None
    operands = []
    for col in zip_longest(*data):
        if set(col) == {" "} or set(col) == {"\n", None}:
            if last_op == "+":
                total += sum(operands)
            elif last_op == "*":
                result = 1
                for n in operands:
                    result *= n
                total += result
            last_op = None
            operands = []
            continue

        if col[-1] in ("+", "*"):
            last_op = col[-1]
            operands = []

        operands.append(int("".join(c for c in col[:-1] if c != " ")))

    print("Step 2:", total)


if __name__ == "__main__":
    step1()
    step2()
    # Attempt 1 - 9302499534581 - too low
    # This Broke it
    # 59   6 67
    # 32  44 44
    # 691 63 367
    # 254 77 298
    # +   +  +
    # Attempt 2 - 9348430857627
