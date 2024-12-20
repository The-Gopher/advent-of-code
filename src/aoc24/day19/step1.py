from pathlib import Path
import re


def main():
    file = Path(__file__).parent / "input"
    # file = Path(__file__).parent / "example"

    towels, patterns = file.read_text().strip().split("\n\n")

    r = "|".join([t.strip() for t in towels.split(",")])
    reg = re.compile(f"^({r})+$")

    count = 0

    for pattern in patterns.splitlines():
        match = reg.match(pattern)
        print(pattern, match)
        if match:
            count += 1

    print(count)


if __name__ == "__main__":
    main()
