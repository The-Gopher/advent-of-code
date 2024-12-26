import enum
from math import pi
from pathlib import Path
from typing import List, Mapping, Dict
from itertools import groupby


def get_patter_match_index(pattern: str, start: int, towels: List[str]) -> List[str]:
    return [t for t in towels if pattern.startswith(t, start)]


def match_pattern(pattern: str, towels: List[str]):
    start_end_maps: Dict[int, List[str]] = {
        start: get_patter_match_index(pattern, start, towels)
        for start in range(len(pattern))
    }

    can_end_here = [True] + ([False] * len(pattern))

    for start in range(1, len(can_end_here)):
        for towel in towels:
            match_start = start - len(towel)
            if match_start < 0:
                continue
            if can_end_here[match_start] and pattern.startswith(towel, match_start):
                can_end_here[start] = True
                break
    return can_end_here[-1]


def main():
    file = Path(__file__).parent / "input"
    # file = Path(__file__).parent / "example"

    towels, patterns = file.read_text().strip().split("\n\n")

    towels = [t.strip() for t in towels.split(",")]

    count = 0

    for pattern in patterns.splitlines():
        match = match_pattern(pattern, towels)
        if match:
            count += 1

    print(count)


if __name__ == "__main__":
    main()
