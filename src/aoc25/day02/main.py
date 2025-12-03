from pathlib import Path
from math import log10, ceil

EXAMPLE_FILE = Path(__file__).parent / "example"
INPUT_FILE = Path(__file__).parent / "input"


def step1():
    total = 0
    text = INPUT_FILE.read_text().strip()
    for line  in text.split(","):
        start, end = map(int, line.split("-"))
        result = sum_in_range(start, end)
        total += result
        print(f"Sum in range {start}-{end}: {result}")
    print(f"Total sum: {total}")


def step2():
    pass


def main():
    step1()


def sum_in_range(start: int, end: int) -> int:
    digits_start = n_to_digits(start)
    digits_end = n_to_digits(end)

    range_sum = 0
    for num_digits in range(digits_start, digits_end + 1):
        base = digits_to_base(num_digits)
        if base is None:
            continue

        range_start = get_digit_range_start(start, num_digits)
        range_end = get_digit_range_end(end, num_digits)

        range_start = (
            range_start % base
            if range_start % base == 0
            else range_start + base - (range_start % base)
        )
        while range_start <= range_end:
            range_sum += range_start
            range_start += base

    return range_sum


def n_to_digits(num: int) -> int:
    if num == 0:
        return 1
    return ceil(log10(num + 1))


def digits_to_base(num_digits: int) -> int | None:
    if num_digits <= 0:
        raise ValueError("Number of digits must be positive")
    if num_digits % 2 != 0:
        return None
    return 10 ** (num_digits // 2) + 1


def get_digit_range_start(start, num_digits):
    return max(start, 10 ** (num_digits - 1))


def get_digit_range_end(end, num_digits):
    return min(end, 10**num_digits - 1)


if __name__ == "__main__":
    main()


assert n_to_digits(0) == 1
assert n_to_digits(1) == 1
assert n_to_digits(9) == 1
assert n_to_digits(10) == 2
assert n_to_digits(99) == 2
assert n_to_digits(100) == 3

assert digits_to_base(2) == 11
assert digits_to_base(4) == 101
assert digits_to_base(1) is None
assert digits_to_base(3) is None

assert get_digit_range_start(11, 2) == 11
assert get_digit_range_end(22, 2) == 22

assert get_digit_range_start(11, 2) == 11
assert get_digit_range_start(5, 2) == 10
assert get_digit_range_end(99, 2) == 99
assert get_digit_range_end(150, 2) == 99


assert sum_in_range(11, 21) == 11
assert sum_in_range(11, 22) == 33
assert sum_in_range(11, 23) == 33

assert sum_in_range(10, 21) == 11
assert sum_in_range(10, 22) == 33
assert sum_in_range(10, 23) == 33

assert sum_in_range(11, 22) == 33
assert sum_in_range(95, 115) == 99
assert sum_in_range(998, 1012) == 1010
assert sum_in_range(1188511880, 1188511890) == 1188511885
assert sum_in_range(222220, 222224) == 222222
assert sum_in_range(1698522, 1698528) == 0
assert sum_in_range(446443, 446449) == 446446
assert sum_in_range(38593856, 38593862) == 38593859
