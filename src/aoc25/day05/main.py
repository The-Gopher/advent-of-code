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

if __name__ == "__main__":
    step1()
