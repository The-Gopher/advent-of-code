from pathlib import Path


INPUT = Path(__file__).parent / "input"
# INPUT = Path(__file__).parent / "example"


def step1():
    data = INPUT.read_text().splitlines()
    current_line = data[0].replace("S", "|")

    total_splits = 0

    for line in data[1:]:
        # Copy down beams into spaces
        new_line: str = "".join(
            "|" if a == "|" and b == "." else b for a, b in zip(current_line, line)
        )

        # Find spliter indexes
        splitters = [
            i
            for i, (a, b) in enumerate(zip(current_line, line))
            if a == "|" and b == "^"
        ]
        for index in splitters:
            if index > 0 and line[index - 1] == ".":
                new_line = new_line[: index - 1] + "|" + new_line[index:]
            if index < len(line) - 1 and line[index + 1] == ".":
                new_line = new_line[: index + 1] + "|" + new_line[index + 2 :]
            total_splits += 1

        current_line = new_line
        print(current_line)

    print("Step 1:", total_splits)


def step2():
    pass


if __name__ == "__main__":
    step1()
    # step2()
