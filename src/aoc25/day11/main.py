from pathlib import Path


def parse_file(file: Path) -> dict[str, list[str]]:
    ret = {}
    for line in file.read_text().splitlines():
        node_from, nodes_to = line.strip().split(": ", 2)
        nodes_to = nodes_to.split(" ")
        ret[node_from] = nodes_to

    return ret


def topological_sort(nodes: dict[str, list[str]]) -> list[str]:
    ret = list(
        {to for _, to_nodes in nodes.items() for to in to_nodes} - set(nodes.keys())
    )

    x = {
        node
        for node, to_nodes in nodes.items()
        if all(to_node in ret for to_node in to_nodes)
    }
    while x:
        ret.extend(sorted(x))
        x = {
            node
            for node, to_nodes in nodes.items()
            if node not in ret and all(to_node in ret for to_node in to_nodes)
        }

    return list(reversed(ret))


def paths_between_nodes(
    nodes: dict[str, list[str]],
    start: str,
    end: str,
) -> int:

    nodes_to_explore = [start]
    total_paths = {start: 1}
    while nodes_to_explore:
        current_node = nodes_to_explore.pop(0)
        for to_node in nodes.get(current_node, []):
            if to_node not in total_paths:
                total_paths[to_node] = 0
                nodes_to_explore.append(to_node)
            total_paths[to_node] += total_paths[current_node]
    return total_paths.get(end, 0)


def step1():
    INPUT = Path(__file__).parent / "input"
    # INPUT = Path(__file__).parent / "example"

    nodes = parse_file(INPUT)
    print("Step 1: ", paths_between_nodes(nodes, "you", "out"))
    assert paths_between_nodes(nodes, "you", "out") == 796


def step2():
    INPUT = Path(__file__).parent / "input"
    # INPUT = Path(__file__).parent / "example_pt2"

    nodes = parse_file(INPUT)

    topologically_sorted = topological_sort(nodes)
    a = (topologically_sorted.index("dac"), "dac")
    b = (topologically_sorted.index("fft"), "fft")

    start = "svr"
    first_node = min(a, b)[1]
    second_node = max(a, b)[1]
    end = "out"

    srv_dac_fft_out = (
        paths_between_nodes(nodes, start, first_node)
        * paths_between_nodes(nodes, first_node, second_node)
        * paths_between_nodes(nodes, second_node, end)
    )
    print("Step 2: ", srv_dac_fft_out)


if __name__ == "__main__":
    step1()
    step2()

# Step 2 Attempt 1: 24282063274560 - too low
