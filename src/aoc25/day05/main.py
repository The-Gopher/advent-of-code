from pathlib import Path

INPUT = Path(__file__).parent / "input"
EXAMPLE = Path(__file__).parent / "example"


def load_file(path: Path) -> tuple[list[tuple[int, int]], list[int]]:
    ranges = []
    values = []
    with path.open() as f:
        for line in f:
            if not line.strip():
                break
            start, end = line.strip().split("-")
            ranges.append((int(start), int(end)))
        for line in f:
            values.append(int(line.strip()))

    return ranges, values


def is_in_ranges(ranges: list[tuple[int, int]], value: int) -> bool:
    for start, end in ranges:
        if start <= value <= end:
            return True
    return False


def step1():
    ranges, values = load_file(INPUT)
    total_fresh = 0
    for value in values:
        if is_in_ranges(ranges, value):
            total_fresh += 1
    print(f"Example: {total_fresh} fresh values")


def step2():
    ranges, _ = load_file(INPUT)
    sorted_ranges = sorted(ranges)
    merged_ranges = []
    current_range = sorted_ranges[0]
    for start, end in sorted_ranges[1:]:
        if start > current_range[1] + 1:
            merged_ranges.append(current_range)
            current_range = (start, end)
        else:
            current_range = (current_range[0], max(current_range[1], end))

    merged_ranges.append(current_range)
    print(
        f"Merged Ranges: {sum(end - start + 1 for start, end in merged_ranges)} total values covered"
    )


if __name__ == "__main__":
    step1()
    step2()
