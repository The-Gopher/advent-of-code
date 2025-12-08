from dataclasses import dataclass
from pathlib import Path
from itertools import combinations


INPUT = Path(__file__).parent / "input"
# INPUT = Path(__file__).parent / "example"


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int


def distance_sq(p1: Point, p2: Point) -> int:
    return abs(p1.x - p2.x) ** 2 + abs(p1.y - p2.y) ** 2 + abs(p1.z - p2.z) ** 2


def step1():
    points_from_file = [
        Point(*map(int, line.strip().split(",")))
        for line in INPUT.read_text().splitlines()
    ]
    pairwise_combinations = combinations(points_from_file, 2)
    pairwise_with_distince = [
        (distance_sq(p1, p2), p1, p2) for p1, p2 in pairwise_combinations
    ]
    sorted_by_distance = sorted(pairwise_with_distince, key=lambda x: x[0])

    circuits: list[set[Point]] = []

    for dist, p1, p2 in sorted_by_distance[:10]:
        assert p1 is not p2

        p1_circuit = set([p1])
        p2_circuit = set([p2])
        for circuit in circuits:
            if p1 in circuit:
                p1_circuit = circuit
            if p2 in circuit:
                p2_circuit = circuit

        updated_circuits = [
            c for c in circuits if c is not p1_circuit and c is not p2_circuit
        ]
        merged_circuit = p1_circuit.union(p2_circuit)
        updated_circuits.append(merged_circuit)
        circuits = updated_circuits

    circuit_sizes = [len(circuit) for circuit in circuits]
    sorted_sizes = sorted(circuit_sizes)[::-1]
    print("Step 1:", sorted_sizes[0] * sorted_sizes[1] * sorted_sizes[2])


def step2():
    points_from_file = [
        Point(*map(int, line.strip().split(",")))
        for line in INPUT.read_text().splitlines()
    ]
    pairwise_combinations = combinations(points_from_file, 2)
    pairwise_with_distince = [
        (distance_sq(p1, p2), p1, p2) for p1, p2 in pairwise_combinations
    ]
    sorted_by_distance = sorted(pairwise_with_distince, key=lambda x: x[0])

    circuits: list[set[Point]] = []

    for dist, p1, p2 in sorted_by_distance:
        assert p1 is not p2

        p1_circuit = set([p1])
        p2_circuit = set([p2])
        for circuit in circuits:
            if p1 in circuit:
                p1_circuit = circuit
            if p2 in circuit:
                p2_circuit = circuit

        updated_circuits = [
            c for c in circuits if c is not p1_circuit and c is not p2_circuit
        ]
        merged_circuit = p1_circuit.union(p2_circuit)
        if len(merged_circuit) == len(points_from_file):
            print("Step 2: ", p1.x * p2.x)
            break
        updated_circuits.append(merged_circuit)
        circuits = updated_circuits


if __name__ == "__main__":
    # step1()
    step2()
