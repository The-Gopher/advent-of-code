from pathlib import Path

INPUT = Path(__file__).parent / "input"
# INPUT = Path(__file__).parent / "example"


def parse_file(file: Path) -> list[tuple[str, list[str]]]:
    ret = []
    for line in file.read_text().splitlines():
        node_from, nodes_to = line.strip().split(": ", 2)
        nodes_to = nodes_to.split(" ")
        ret.append((node_from, nodes_to))

    return ret


def step1():
    nodes = parse_file(INPUT)

    total_paths = {"out": 1}

    while len(total_paths) < len(nodes):
        for node, to_nodes in nodes:
            paths_to_out = [total_paths.get(to_node, None) for to_node in to_nodes]
            if None in paths_to_out:
                continue

            total_paths[node] = sum(paths_to_out)

    print("Step 1: ", total_paths["you"])


def step2():
    pass


if __name__ == "__main__":
    step1()
    step2()
