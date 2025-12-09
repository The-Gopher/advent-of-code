from pathlib import Path
from itertools import combinations, pairwise, chain

INPUT = Path(__file__).parent / "input"
# INPUT = Path(__file__).parent / "example"


def step1():
    red_tiles = [
        (int(a), int(b))
        for a, b in (pair.split(",") for pair in INPUT.read_text().splitlines())
    ]
    pairs = list(combinations(red_tiles, 2))
    areas = [
        ((abs(x1 - x2) + 1) * (abs(y1 - y2) + 1), (x1, y1), (x2, y2))
        for (x1, y1), (x2, y2) in pairs
    ]
    print(max(areas))


def step2():
    print("Parse Red Input")
    red_tiles = [
        (int(a), int(b))
        for a, b in (pair.split(",") for pair in INPUT.read_text().splitlines())
    ]

    print("Compute Green Tile Perimeter")
    green_tiles = set()
    for a, b in pairwise(chain(red_tiles, [red_tiles[0]])):
        if a[0] == b[0]:
            for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
                tile = (a[0], y)
                if tile not in red_tiles:
                    green_tiles.add((a[0], y))
        elif a[1] == b[1]:
            for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
                tile = (x, a[1])
                if tile not in red_tiles:
                    green_tiles.add((x, a[1]))
        else:
            raise ValueError("Non axis-aligned edge")

    x_max = max(x for x, y in green_tiles)
    y_max = max(y for x, y in green_tiles)

    print(x_max, y_max)

    print("Fill Interior with Green Tiles")
    if False:
        for row in range(y_max + 1):
            green_tiles_in_row = [(x, y) for x, y in green_tiles if y == row]
            if not green_tiles_in_row:
                continue

            x_min = min([x for x, y in green_tiles_in_row])
            x_max = max([x for x, y in green_tiles_in_row])

            for x in range(x_min, x_max + 1):
                if (x, row) not in red_tiles and (x, row) not in green_tiles:
                    green_tiles.add((x, row))

    print("Render Tiles")
    assert set(red_tiles).isdisjoint(green_tiles)
    for y in range(y_max + 2):
        row = ""
        for x in range(x_max + 2):
            if (x, y) in green_tiles:
                row += "G"
            elif (x, y) in red_tiles:
                row += "R"
            else:
                row += "."
        print(row)


if __name__ == "__main__":
    step1()
    step2()
