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
    topological_sorted = topological_sort(nodes)
    nodes_to_explore = [start]
    total_paths = {start: 1}
    while nodes_to_explore:
        current_node = nodes_to_explore.pop(0)
        for to_node in nodes.get(current_node, []):
            if to_node not in total_paths:
                total_paths[to_node] = 0
                nodes_to_explore.append(to_node)
            total_paths[to_node] += total_paths[current_node]

        nodes_to_explore = [n for n in topological_sorted if n in nodes_to_explore]

    return total_paths.get(end, 0)


def step1():
    INPUT = Path(__file__).parent / "input"
    # INPUT = Path(__file__).parent / "example"
    # INPUT = Path(__file__).parent / "test_case1"

    nodes = parse_file(INPUT)
    print("Step 1: ", paths_between_nodes(nodes, "you", "out"))
    assert paths_between_nodes(nodes, "you", "out") == 796, paths_between_nodes(
        nodes, "you", "out"
    )


def step2():
    INPUT = Path(__file__).parent / "input"
    # INPUT = Path(__file__).parent / "example_pt2"

    nodes = parse_file(INPUT)

    srv_fft_dac_out = (
        paths_between_nodes(nodes, "svr", "fft")
        * paths_between_nodes(nodes, "fft", "dac")
        * paths_between_nodes(nodes, "dac", "out")
    )
    print("srv_fft_dac_out: ", srv_fft_dac_out)

    srv_dac_fft_out = (
        paths_between_nodes(nodes, "svr", "dac")
        * paths_between_nodes(nodes, "dac", "fft")
        * paths_between_nodes(nodes, "fft", "out")
    )
    print("srv_dac_fft_out: ", srv_dac_fft_out)

    step2_result = srv_fft_dac_out + srv_dac_fft_out

    assert step2_result > 24282063274560
    print("Step 2: ", step2_result)


if __name__ == "__main__":
    step1()
    step2()

# Step 2 Attempt 1: 24282063274560 - too low
# Step 2 Attempt 2: 294053029111296