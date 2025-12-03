from pathlib import Path

EXAMPLE_FILE = Path(__file__).parent / "example"
INPUT_FILE = Path(__file__).parent / "input"


def step(max: str, rest: str) -> str:
    if rest == "":
        return max

    next_char = rest[0]
    rest = rest[1:]

    int_max = int(max)

    if int(max[1] + next_char) > int_max:
        return step(max[1] + next_char, rest)
    elif int(max[0] + next_char) > int_max:
        return step(max[0] + next_char, rest)
    else:
        return step(max, rest)


def line_to_max_joltage(line: str) -> int:
    return int(step(line[:2], line[2:]))


def step1():
    print(
        "Step 1: ",
        sum(line_to_max_joltage(line) for line in INPUT_FILE.read_text().splitlines()),
    )


if __name__ == "__main__":
    step1()

assert line_to_max_joltage("987654321111111") == 98
assert line_to_max_joltage("811111111111119") == 89
assert line_to_max_joltage("234234234234278") == 78
assert line_to_max_joltage("818181911112111") == 92
