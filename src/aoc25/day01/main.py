from pathlib import Path


START = 50
SIZE = 100
EXAMPLE_FILE = Path(__file__).parent / "example"
INPUT_FILE = Path(__file__).parent / "input"


def parse_line(line: str) -> int:
    dir = line[0]
    value = line[1:]
    if dir == "L":
        return -int(value.strip())
    return int(value.strip())


def step1():
    current_point = START
    crossing = 0
    for line in INPUT_FILE.read_text().strip().split("\n"):
        rotate = parse_line(line)

        next_point = current_point + rotate
        current_point = next_point % SIZE
        if current_point == 0:
            crossing += 1

    print(crossing)


def step2():
    current_point = START
    crossing = 0
    for line in INPUT_FILE.read_text().strip().split("\n"):
        rotate = parse_line(line)
        crossing += count_crossings(current_point, rotate)
        current_point = (current_point + rotate) % SIZE

    print(crossing)


def count_crossings(start, direction) -> int:
    if direction < 0:
        return count_crossings_left(start, direction)
    else:
        return count_crossings_right(start, direction)


def count_crossings_left(start, direction) -> int:
    crossings = abs(direction) // SIZE
    net_turns = -(abs(direction) % SIZE)
    additional_crossing = 1 if start > 0 and (start + net_turns) <= 0 else 0
    return crossings + additional_crossing


def count_crossings_right(start, direction) -> int:
    crossings = direction // SIZE
    net_turns = direction % SIZE
    additional_crossing = 1 if (start + net_turns) >= SIZE else 0
    return crossings + additional_crossing


def main():
    step2()


if __name__ == "__main__":
    main()

assert count_crossings(50, -49) == 0
assert count_crossings(50, -50) == 1
assert count_crossings(50, 49) == 0
assert count_crossings(50, 50) == 1

assert count_crossings(0, 99) == 0
assert count_crossings(0, 100) == 1
assert count_crossings(0, 101) == 1
assert count_crossings(0, 199) == 1
assert count_crossings(0, 200) == 2
assert count_crossings(0, 201) == 2

assert count_crossings(0, -99) == 0
assert count_crossings(0, -100) == 1
assert count_crossings(0, -101) == 1
assert count_crossings(0, -199) == 1
assert count_crossings(0, -200) == 2
assert count_crossings(0, -201) == 2

assert count_crossings(1, 98) == 0
assert count_crossings(1, 99) == 1
assert count_crossings(1, 100) == 1
assert count_crossings(1, 199) == 2
assert count_crossings(1, 200) == 2
assert count_crossings(1, 201) == 2

# Step 2 - 
# Attempt 1 - 6334 - High
# Attempt 2 - 6133 - Correct