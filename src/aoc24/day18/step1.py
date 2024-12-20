from itertools import pairwise, chain
from pathlib import Path
from typing import List, Tuple, Dict, Set
from colorama import Back, Fore, Style
import heapq


DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
DIRECTION_MAP = {
    "^": (0, -1),
    "v": (0, 1),
    ">": (1, 0),
    "<": (-1, 0),
}


def walls_to_maze(walls_raw: List[str]) -> List[Tuple[int, int]]:
    return [(int(x), int(y)) for x, y in (line.split(",") for line in walls_raw)]


def draw(
    maze: List[Tuple[int, int]],
    path: List[Tuple[int, int]],
    min_map: Dict[Tuple[int, int], int],
    size: int,
):
    for y in range(size):
        for x in range(size):
            if (x, y) in maze:
                print("#", end="")
            elif (x, y) in path:
                print(Fore.RED + "O" + Fore.RESET, end="")
            elif (x, y) in min_map:
                print(Fore.RED + "." + Fore.RESET, end="")
            else:
                print(".", end="")
        print(Style.RESET_ALL)


def score_path(path: List[Tuple[int, int]]) -> int:
    return len(path)


def find_shortest_path(maze, start, end, size) -> int | None:
    heap: List[Tuple[int, int, Tuple[int, int]]] = [(0, 1, start)]

    min_map: Dict[Tuple[int, int], int] = {}

    best_paths: List[List[Tuple[int, int]]] = []
    best_score = None

    while len(heap) > 0:
        _heuristic, score, pos = heapq.heappop(heap)

        if best_score and score > best_score:
            break

        if pos == end:
            best_score = score
            best_paths.append([])

        for d in DIRECTIONS:
            new_pos = (pos[0] + d[0], pos[1] + d[1])

            if (
                new_pos[0] < 0
                or new_pos[0] >= size
                or new_pos[1] < 0
                or new_pos[1] >= size
            ):
                continue

            if new_pos in maze:
                continue

            # new_path = path + [new_pos]
            new_score = score + 1

            key = new_pos
            if key not in min_map:
                min_map[key] = new_score
            elif new_score < min_map[key]:
                min_map[key] = new_score
            else:
                continue

            guess = new_score + abs(new_pos[0] - end[0]) + abs(new_pos[1] - end[1])

            heapq.heappush(heap, (guess, new_score, new_pos))

    return best_score


def main():
    file, size, limit = Path(__file__).parent / "input", 71, 1024
    # file, size, limit = Path(__file__).parent / "example", 7, 12

    start = (0, 0)
    end = (size - 1, size - 1)

    maze = walls_to_maze(file.read_text().splitlines())
    total_length = len(maze)

    low, mid, high = 0, total_length // 2, total_length
    while low != high:
        print(low, mid, high)
        partial_maze = maze[:mid]
        distance = find_shortest_path(partial_maze, start, end, size)

        if distance:
            low, mid, high = mid, (mid + high) // 2, high
        else:
            low, mid, high = low, (low + mid) // 2, mid - 1

    partial_maze = maze[:mid]
    print(find_shortest_path(partial_maze, start, end, size))

    partial_maze = maze[: mid + 1]
    print(find_shortest_path(partial_maze, start, end, size))
    print(partial_maze[-1])


if __name__ == "__main__":
    main()
