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
    print(total)


if __name__ == "__main__":
    step1()
