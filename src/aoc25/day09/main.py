import enum
from operator import le
from pathlib import Path
from itertools import chain, combinations, pairwise
from re import X
from progress.bar import Bar

INPUT = Path(__file__).parent / "input"
# INPUT = Path(__file__).parent / "example"


def compute_area(
    mapping_x: dict[int, int],
    mapping_y: dict[int, int],
    p1: tuple[int, int],
    p2: tuple[int, int],
) -> int:
    (x1_idx, y1_idx) = p1
    (x2_idx, y2_idx) = p2

    x1 = mapping_x[x1_idx]
    x2 = mapping_x[x2_idx]

    y1 = mapping_y[y1_idx]
    y2 = mapping_y[y2_idx]

    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)


def points_in_rectangle(
    rect: tuple[tuple[int, int], tuple[int, int]], all_points: set[tuple[int, int]]
) -> set[tuple[int, int]]:
    p1, p2 = rect
    (x1, y1) = p1
    (x2, y2) = p2

    points: set[tuple[int, int]] = set()
    for p in all_points:
        (px, py) = p
        if min(x1, x2) < px < max(x1, x2) and min(y1, y2) < py < max(y1, y2):
            points.add(p)
    return points


def print_rectangle(
    size: tuple[int, int],
    red_points: list[tuple[int, int]],
    corners: tuple[tuple[int, int], tuple[int, int]],
) -> None:
    size_x, size_y = size

    for y in range(size_y):
        row = ""
        for x in range(size_x):
            if (x, y) in corners:
                row += "C"
            elif (x, y) in red_points:
                row += "R"
            else:
                row += "."
        print(row)


def step1():
    red_tiles = [
        (int(a), int(b))
        for a, b in (pair.split(",") for pair in INPUT.read_text().splitlines())
    ]

    x_to_x_rank: dict[int, int] = {
        x: idx for idx, x in enumerate(sorted([x for x, y in red_tiles]), 1)
    }
    x_rank_to_x: dict[int, int] = {idx: x for x, idx in x_to_x_rank.items()}

    y_to_y_rank: dict[int, int] = {
        y: idx for idx, y in enumerate(sorted([y for x, y in red_tiles]), 1)
    }
    y_rank_to_y: dict[int, int] = {idx: y for y, idx in y_to_y_rank.items()}

    red_tiles_idx = [(x_to_x_rank[x], y_to_y_rank[y]) for x, y in red_tiles]

    pairs = list(combinations(red_tiles_idx, 2))
    areas = [
        (compute_area(x_rank_to_x, y_rank_to_y, (x1, y1), (x2, y2)), (x1, y1), (x2, y2))
        for (x1, y1), (x2, y2) in pairs
    ]
    print(max(areas))


def step2():
    print("Parse Red Input")
    red_tiles = [
        (int(a), int(b))
        for a, b in (pair.split(",") for pair in INPUT.read_text().splitlines())
    ]

    x_to_x_rank: dict[int, int] = {
        x: idx for idx, x in enumerate(sorted([x for x, y in red_tiles]), 1)
    }
    y_to_y_rank: dict[int, int] = {
        y: idx for idx, y in enumerate(sorted([y for x, y in red_tiles]), 1)
    }

    print(len(x_to_x_rank))
    print(len(y_to_y_rank))

    red_tiles_idx = [(x_to_x_rank[x], y_to_y_rank[y]) for x, y in red_tiles]

    bar = Bar("Compute Green Tiles")
    green_tiles_idx: set[tuple[int, int]] = set()
    for p1, p2 in bar.iter(pairwise(chain(red_tiles_idx, [red_tiles_idx[0]]))):
        (x1, y1) = p1
        (x2, y2) = p2

        if x1 == x2:
            for y in range(min(y1, y2) + 1, max(y1, y2)):
                green_tiles_idx.add((x1, y))
        elif y1 == y2:
            for x in range(min(x1, x2) + 1, max(x1, x2)):
                green_tiles_idx.add((x, y1))
    print("Green Tiles: ", len(green_tiles_idx))

    x_rank_to_x: dict[int, int] = {idx: x for x, idx in x_to_x_rank.items()}
    y_rank_to_y: dict[int, int] = {idx: y for y, idx in y_to_y_rank.items()}

    pairs = list(combinations(red_tiles_idx, 2))
    areas: list[tuple[int, tuple[int, int], tuple[int, int]]] = []
    bar = Bar("Finding Max Area")
    for p1, p2 in bar.iter(pairs):
        points_in_rect = points_in_rectangle((p1, p2), green_tiles_idx)

        if points_in_rect:
            continue

        area = compute_area(x_rank_to_x, y_rank_to_y, p1, p2)
        areas.append((area, p1, p2))

    print(max(areas))


if __name__ == "__main__":
    step1()
    step2()
