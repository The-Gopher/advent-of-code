from hmac import new
from pathlib import Path
from socket import inet_aton
from turtle import width
from typing import Literal, Tuple, Set


DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
DIRECTION_MAP = {
    "^": (0, -1),
    "v": (0, 1),
    ">": (1, 0),
    "<": (-1, 0),
}


EXAMPLE_OUTPUT = """####################
##[].......[].[][]##
##[]...........[].##
##[]........[][][]##
##[]......[]....[]##
##..##......[]....##
##..[]............##
##..@......[].[][]##
##......[][]..[]..##
####################"""
EXAMPLE_BLOCKS = {
    (x * 2, y)
    for y, line in enumerate(EXAMPLE_OUTPUT.splitlines())
    for x, c in enumerate(line)
    if c == "O"
}


def parse_map(map):
    print(map)
    map = map.splitlines()

    height = len(map)
    width = len(map[0]) * 2

    walls = {
        (x * 2 + i, y)
        for i in (0, 1)
        for y, line in enumerate(map)
        for x, c in enumerate(line)
        if c == "#"
    }
    blocks = {
        (x * 2, y) for y, line in enumerate(map) for x, c in enumerate(line) if c == "O"
    }
    robot = [
        (x * 2, y) for y, line in enumerate(map) for x, c in enumerate(line) if c == "@"
    ]

    assert len(robot) == 1
    robot = robot[0]

    return walls, blocks, robot, height, width


def draw(walls, blocks, robot, width, height):

    for i in range(height):
        print(f"{i:03d} ", end="")

        for j in range(width):
            x = "."
            if (j, i) in walls:
                x = "#"
            elif (j, i) in blocks:
                x = "["
            elif (j - 1, i) in blocks:
                x = "]"
            elif (j, i) == robot:
                x = "@"
            print(x, end="")

        print("")


def move(
    walls: Set[Tuple[int, int]],
    blocks: Set[Tuple[int, int]],
    robot: Tuple[int, int],
    direction,
):
    if direction == "<":
        return move_left(walls, blocks, robot)
    elif direction == ">":
        return move_right(walls, blocks, robot)
    elif direction == "^":
        return move_v(walls, blocks, robot, -1)
    elif direction == "v":
        return move_v(walls, blocks, robot, 1)

    raise ValueError(f"Unknown direction {direction}")


def move_left(
    walls: Set[Tuple[int, int]],
    blocks: Set[Tuple[int, int]],
    robot: Tuple[int, int],
):
    blocks_to_move: Set[Tuple[int, int]] = set()
    next_robot = robot[0] - 1, robot[1]
    i = robot[0] - 2, robot[1]

    while True:
        if i in walls:
            return walls, blocks, robot
        if i not in blocks:
            break
        blocks_to_move.add(i)
        i = i[0] - 2, i[1]
    new_ret: Set[Tuple[int, int]] = {(b[0] - 1, b[1]) for b in blocks_to_move}
    return walls, blocks - blocks_to_move | new_ret, next_robot


def move_right(
    walls: Set[Tuple[int, int]],
    blocks: Set[Tuple[int, int]],
    robot: Tuple[int, int],
):
    blocks_to_move: Set[Tuple[int, int]] = set()
    next_robot = robot[0] + 1, robot[1]
    i = next_robot

    while True:
        if i in walls:
            return walls, blocks, robot
        if i not in blocks:
            break
        blocks_to_move.add(i)
        i = i[0] + 2, i[1]
    new_ret: Set[Tuple[int, int]] = {(b[0] + 1, b[1]) for b in blocks_to_move}
    return walls, blocks - blocks_to_move | new_ret, next_robot


def move_v(
    walls: Set[Tuple[int, int]],
    blocks: Set[Tuple[int, int]],
    robot: Tuple[int, int],
    d: Literal[1, -1],
):
    blocks_to_move: Set[Tuple[int, int]] = set()
    next_robot = robot[0], robot[1] + d
    next_wall_check = {next_robot}
    next_block_check = {
        (next_robot[0] - 1, next_robot[1]),
        (next_robot[0] + 0, next_robot[1]),
    }

    while True:
        next_block_intersection = next_block_check.intersection(blocks)

        if next_wall_check.intersection(walls) or len(next_block_intersection) > 1:
            return walls, blocks, robot

        if not next_block_intersection:
            break

        block_to_move = next_block_intersection.pop()
        blocks_to_move.add(block_to_move)

        new_block = block_to_move[0], block_to_move[1] + d
        next_wall_check = {new_block, (new_block[0] + 1, new_block[1])}
        next_block_check = next_wall_check | {(new_block[0] - 1, new_block[1])}

    if len(blocks_to_move) > 1:
        return walls, blocks, robot
    new_ret: Set[Tuple[int, int]] = {(b[0], b[1] + d) for b in blocks_to_move}
    return walls, blocks - blocks_to_move | new_ret, next_robot


def validate_map(
    walls: Set[Tuple[int, int]],
    blocks: Set[Tuple[int, int]],
    robot: Tuple[int, int],
    width,
    height,
):
    alt_blocks = {(x + 1, y) for x, y in blocks}
    if walls.intersection(alt_blocks):
        draw(walls, blocks, robot, width, height)
        raise ValueError("Invalid map")
    if blocks.intersection(alt_blocks):
        draw(walls, blocks, robot, width, height)
        raise ValueError("Invalid map")
    if robot in walls or robot in blocks or robot in alt_blocks:
        draw(walls, blocks, robot, width, height)
        raise ValueError("Invalid map")


def main():
    file = Path(__file__).parent / "input"
    file = Path(__file__).parent / "example"

    map, actions = file.read_text().split("\n\n")

    walls, blocks, robot, height, width = parse_map(map)

    draw(walls, blocks, robot, width, height)
    # input()

    for action in actions:
        if action in DIRECTION_MAP:
            print(action)
            walls, blocks, robot = move(walls, blocks, robot, action)
            validate_map(walls, blocks, robot, width, height)
            draw(walls, blocks, robot, width, height)
            input()

    draw(walls, blocks, robot, width, height)
    print(sum(x + 100 * y for x, y in blocks))


if __name__ == "__main__":
    main()
