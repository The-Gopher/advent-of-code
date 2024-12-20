from itertools import pairwise, chain
from pathlib import Path
from typing import List, Tuple, Dict, Set
from colorama import Fore, Style
import heapq


DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
DIRECTION_MAP = {
    "^": (0, -1),
    "v": (0, 1),
    ">": (1, 0),
    "<": (-1, 0),
}


def walls_to_maze(
    walls_raw: List[str], size: int, limit: int | None = None
) -> List[str]:
    walls: List[Tuple[int, int]] = [
        (int(x), int(y))
        for x, y in (
            line.split(",")
            for line in ((walls_raw[:limit] if limit is not None else walls_raw))
        )
    ]

    return [
        "".join(["#" if (x, y) in walls else "." for x in range(size)])
        for y in range(size)
    ]


def draw(maze: List[str], path: Set[Tuple[int, int]]):
    for y, line in enumerate(maze):
        for x, c in enumerate(line):
            if (x, y) in path:
                print(Fore.RED + c + Fore.RESET, end="")
            else:
                print(c, end="")
        print(Style.RESET_ALL)


def score_path(path: List[Tuple[int, int]]) -> int:
    return len(path)


def main():
    file, size, limit = Path(__file__).parent / "input", 71, 1024
    # file, size, limit = Path(__file__).parent / "example", 7, 12

    maze = walls_to_maze(file.read_text().splitlines(), size, limit)
    draw(maze, set())

    start = (0, 0)
    end = (size - 1, size - 1)

    heap: List[Tuple[int, Tuple[int, int], List[Tuple[int, int]]]] = [
        (0, start, [start])
    ]

    min_map: Dict[Tuple[int, int], int] = {}

    best_paths: List[List[Tuple[int, int]]] = []
    best_score = None

    while True:
        score, pos, path = heapq.heappop(heap)

        print(score)

        if best_score and score > best_score:
            break

        if pos == end:
            assert score == score_path(path)
            best_score = score
            best_paths.append(path)

        for d in DIRECTIONS:
            new_pos = (pos[0] + d[0], pos[1] + d[1])

            if (
                new_pos[0] < 0
                or new_pos[0] >= size
                or new_pos[1] < 0
                or new_pos[1] >= size
            ):
                continue

            if maze[new_pos[1]][new_pos[0]] == "#":
                continue

            if new_pos in path:
                continue

            new_path = path + [new_pos]
            new_score = score_path(new_path)

            key = new_pos
            if (key in min_map) and (new_score > min_map[key]):
                continue
            min_map[key] = new_score

            heapq.heappush(heap, (new_score, new_pos, new_path))

    print(best_score - 1)

    path = best_paths[0]
    draw(maze, set(path))


if __name__ == "__main__":
    main()
