from collections import Counter, defaultdict
from email.policy import default
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

DIRECTIONS_2 = {
    (ax + bx, ay + by)
    for ax, ay in DIRECTIONS
    for bx, by in DIRECTIONS
    if ax + bx or ay + by
}


def find_point(maze: List[str], point: str) -> Tuple[int, int] | None:
    for y, line in enumerate(maze):
        x = line.find(point)
        if x != -1:
            return x, y
    return None


def draw(maze: List[str], path: List[Tuple[int, int]]):
    for y, line in enumerate(maze):
        for x, c in enumerate(line):
            if (x, y) in path:
                print(Fore.RED + c + Fore.RESET, end="")
            else:
                print(c, end="")
        print(Style.RESET_ALL)


def score_path(path: List[Tuple[int, int]]) -> int:
    return len(path) - 1


def main():
    file, expected = Path(__file__).parent / "input", None
    # file, expected = Path(__file__).parent / "example_2", 11048
    # file, expected = Path(__file__).parent / "example", None

    maze = file.read_text().splitlines()

    start = find_point(maze, "S")
    end = find_point(maze, "E")

    if start is None or end is None:
        raise ValueError("Start or end not found")

    heap: List[Tuple[int, Tuple[int, int], List[Tuple[int, int]]]] = [
        (0, start, [start])
    ]

    min_map: Dict[Tuple[int, int], int] = {}

    best_paths: List[List[Tuple[int, int]]] = []
    best_score = None

    while heap:
        score, pos, path = heapq.heappop(heap)

        if best_score and score > best_score:
            break

        if pos == end:
            assert score == score_path(path)
            best_score = score
            best_paths.append(path)

        for d in DIRECTIONS:
            new_pos = (pos[0] + d[0], pos[1] + d[1])
            if maze[new_pos[1]][new_pos[0]] == "#":
                continue
            if new_pos in path:
                continue

            new_path = path + [new_pos]
            new_score = score_path(new_path)

            if (new_pos in min_map) and (new_score > min_map[new_pos]):
                continue
            min_map[new_pos] = new_score

            heapq.heappush(heap, (new_score, new_pos, new_path))

    path: List[Tuple[int, int]] = best_paths[0]
    point_distances = {path[i]: score_path(path[i:]) for i in range(len(path))}

    for p in point_distances.items():
        print(p)

    count = 0
    for p in path:
        px, py = p

        for dx, dy in DIRECTIONS_2:

            new_point = (px + dx, py + dy)
            if new_point not in point_distances:
                continue

            shortcut_gain = point_distances[p] - point_distances[new_point] - 2

            if shortcut_gain <= 0:
                continue

            if shortcut_gain >= 100:
                count += 1

    print(count)


if __name__ == "__main__":
    main()
