from pathlib import Path


EXAMPLE_FILE = Path(__file__).parent / "example"
INPUT_FILE = Path(__file__).parent / "input"


def drop_i(s: str, i: int) -> str:
    return s[:i] + s[i + 1 :]


def step(current: str, rest: str) -> str:
    if rest == "":
        return current

    next_char = rest[0]
    rest = rest[1:]

    max = current
    int_max = int(max)
    for i in range(len(current)):
        i_str = drop_i(current, i) + next_char
        i_int = int(i_str)
        if i_int > int_max:
            max = i_str
            int_max = i_int

    return step(max, rest)


def line_to_max_joltage(line: str) -> int:
    return int(step(line[:2], line[2:]))


def step1():
    print(
        "Step 1: ",
        sum(line_to_max_joltage(line) for line in INPUT_FILE.read_text().splitlines()),
    )


def line_to_max_joltage_12(line: str) -> int:
    return int(step(line[:12], line[12:]))


def step2():
    print(
        "Step 2: ",
        sum(
            line_to_max_joltage_12(line) for line in INPUT_FILE.read_text().splitlines()
        ),
    )


if __name__ == "__main__":
    step1()
    step2()

assert line_to_max_joltage("987654321111111") == 98
assert step("81", "9") == "89"
assert line_to_max_joltage("811111111111119") == 89
assert line_to_max_joltage("234234234234278") == 78
assert line_to_max_joltage("818181911112111") == 92

# 811111111111119
# 811111111111
assert step("811111111111", "119") == "811111111119"
assert line_to_max_joltage_12("987654321111111") == 987654321111
assert line_to_max_joltage_12("811111111111119") == 811111111119
assert line_to_max_joltage_12("234234234234278") == 434234234278
assert line_to_max_joltage_12("818181911112111") == 888911112111
