from collections import Counter
from pathlib import Path
from itertools import chain, combinations, pairwise
from progress.bar import Bar
import re
import dataclasses

INPUT = Path(__file__).parent / "input"
# INPUT = Path(__file__).parent / "example"

# [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
regex = re.compile(r"^\[([\.#]+)\] ([\(\) 0-9,]+) \{([0-9,]+)\}$")


@dataclasses.dataclass
class Line:
    light_pattern: str
    buttons: list[set[int]]
    power: list[int]


def count_required_buttons(line: Line) -> int:
    required_pattern = {i for i, c in enumerate(line.light_pattern) if c == "#"}
    for button_count in range(1, len(line.buttons) + 1):
        for button_combination in combinations(range(len(line.buttons)), button_count):
            toggled = Counter(
                [
                    i
                    for button_index in button_combination
                    for i in line.buttons[button_index]
                ]
            )

            on_lights = {a for a, b in toggled.items() if b % 2 == 1}
            if on_lights == required_pattern:
                return button_count

    raise ValueError("No combination found")


def step1():
    lines = [
        Line(
            light_pattern=match.group(1),
            buttons=[
                (
                    set(int(x) for x in group.strip().split(","))
                    if group.strip()
                    else set()
                )
                for group in match.group(2).strip(" ()").replace(" ", "").split(")(")
            ],
            power=[int(x) for x in match.group(3).strip().split(",")],
        )
        for match in [regex.match(line) for line in INPUT.read_text().splitlines()]
        if match
    ]
    result = 0
    for line in lines:
        result += count_required_buttons(line)

    print(result)


def step2():
    pass


if __name__ == "__main__":
    step1()
    step2()
