from hmac import new
from itertools import pairwise
from pathlib import Path


INPUT = Path(__file__).parent / "input"
# INPUT = Path(__file__).parent / "example"


def step1():
    data = INPUT.read_text().splitlines()
    current_line = data[0].replace("S", "|")

    total_splits = 0

    for line in data[1:]:
        # Copy down beams into spaces
        new_line: str = "".join(
            "|" if a == "|" and b == "." else b for a, b in zip(current_line, line)
        )

        # Find spliter indexes
        splitters = [
            i
            for i, (a, b) in enumerate(zip(current_line, line))
            if a == "|" and b == "^"
        ]
        for index in splitters:
            if index > 0 and line[index - 1] == ".":
                new_line = new_line[: index - 1] + "|" + new_line[index:]
            if index < len(line) - 1 and line[index + 1] == ".":
                new_line = new_line[: index + 1] + "|" + new_line[index + 2 :]
            total_splits += 1

        current_line = new_line
        print(current_line)

    print("Step 1:", total_splits)
    # Step 1: 1579


def step2():
    data = INPUT.read_text().splitlines()
    current_line = data[0].replace("S", "|")

    beam_map = [current_line]

    for line in data[1:]:
        # Copy down beams into spaces
        new_line: str = "".join(
            "|" if a == "|" and b == "." else b for a, b in zip(current_line, line)
        )

        # Find spliter indexes
        splitters = [
            i
            for i, (a, b) in enumerate(zip(current_line, line))
            if a == "|" and b == "^"
        ]
        for index in splitters:
            if index > 0 and line[index - 1] == ".":
                new_line = new_line[: index - 1] + "|" + new_line[index:]
            if index < len(line) - 1 and line[index + 1] == ".":
                new_line = new_line[: index + 1] + "|" + new_line[index + 2 :]

        current_line = new_line
        beam_map.append(current_line)

    beam_map = list(reversed(beam_map))
    current_line: list[int] = [1 if c == "|" else 0 for c in beam_map[0]]
    for top_line, bottom_line in pairwise(beam_map):

        new_line: list[int] = [0 for _ in current_line]
        for index, count in enumerate(current_line):
            if top_line[index] != "|":
                continue

            # Beam propagates down
            if bottom_line[index] == "|":
                new_line[index] += count

            # Beam split moving right
            if (
                index > 0
                and top_line[index - 1] == "^"
                and bottom_line[index - 1] == "|"
            ):
                new_line[index - 1] += count

            # Beam split moving left
            if (
                index < len(top_line) - 1
                and top_line[index + 1] == "^"
                and bottom_line[index + 1] == "|"
            ):
                new_line[index + 1] += count

        current_line = new_line

    print(current_line)


if __name__ == "__main__":
    # step1()
    step2()
