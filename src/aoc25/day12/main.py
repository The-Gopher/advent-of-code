from functools import cached_property
from pathlib import Path
from dataclasses import dataclass

INPUT = Path(__file__).parent / "input"
# INPUT = Path(__file__).parent / "example"


@dataclass(frozen=True)
class Shape:
    grid: tuple[
        tuple[bool, bool, bool], tuple[bool, bool, bool], tuple[bool, bool, bool]
    ]

    @cached_property
    def area(self) -> int:
        return sum(sum(1 for cell in row if cell) for row in self.grid)


ShapeRequirements = tuple[int, int, int, int, int, int]


@dataclass(frozen=True)
class AreaWithRequirements:
    width: int
    height: int

    shape_requirements: ShapeRequirements
    shapes: tuple[Shape, Shape, Shape, Shape, Shape, Shape]

    @cached_property
    def area(self) -> int:
        return self.width * self.height

    @cached_property
    def total_required_area(self) -> int:
        return sum(
            shape.area * count
            for shape, count in zip(self.shapes, self.shape_requirements)
        )

    @cached_property
    def slop_area(self) -> int:
        return self.area - self.total_required_area


def parse_input(
    input_path,
) -> list[AreaWithRequirements]:
    shapes: list[Shape] = []
    areas: list[AreaWithRequirements] = []
    with open(input_path, "r") as f:
        for i in range(6):
            shape_number = int(f.readline().strip().strip(":"))
            assert shape_number == i

            line1 = tuple(c == "#" for c in f.readline().strip())
            line2 = tuple(c == "#" for c in f.readline().strip())
            line3 = tuple(c == "#" for c in f.readline().strip())

            assert len(line1) == 3
            assert len(line2) == 3
            assert len(line3) == 3

            shapes.append(Shape((line1, line2, line3)))
            f.readline()

        shapes_tuple = tuple(shapes)
        assert len(shapes_tuple) == 6

        for line in f:
            area, shape = line.strip().split(": ")
            area_x, area_y = tuple(int(x) for x in area.split("x"))
            shapes_required = tuple(int(x) for x in shape.split(" "))

            assert len(shapes_required) == 6

            areas.append(
                AreaWithRequirements(area_x, area_y, shapes_required, shapes_tuple)
            )

    return areas


def step1():
    areas = parse_input(INPUT)

    can_fit = [a for a in areas if a.total_required_area <= a.area]
    print("Areas that can fit all required shapes:", len(can_fit))


def step2():
    pass


if __name__ == "__main__":
    step1()
    step2()
