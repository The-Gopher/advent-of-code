import enum
from numpy import array, convolve, sum
from pathlib import Path
import scipy.ndimage
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)

EXAMPLE_FILE = Path(__file__).parent / "example"
EXAMPLE_OUTPUT_FILE = Path(__file__).parent / "example_output"

INPUT_FILE = Path(__file__).parent / "input"


def input_to_array(file_str: str) -> array:
    return array(
        [
            [1 if char == "@" else 0 for char in line.strip()]
            for line in file_str.splitlines()
        ]
    )


def print_array(arr: array):
    print("==========")
    for row in arr:
        print("".join(["@" if cell == 1 else "." for cell in row]))
    print()


def count_neighbors(arr: array) -> array:
    mask = array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    neighbors = scipy.ndimage.correlate(arr, mask, mode="constant", cval=0)
    return np.multiply(arr, neighbors)


def step1():
    data = input_to_array(INPUT_FILE.read_text())
    data = count_neighbors(data)

    data[data == 0] = 7
    data[data <= 4] = 1
    data[data != 1] = 0

    print(sum(data))


if __name__ == "__main__":
    step1()


def test_case1():
    one_by_one = input_to_array("@")
    one_by_one_step1 = count_neighbors(one_by_one)
    print(one_by_one_step1)

    assert input_to_array("@").shape == (1, 1)


def test_case3_0():
    three_by_three = input_to_array("...\n.@.\n...")
    three_by_three_step1 = count_neighbors(three_by_three)
    print(three_by_three_step1)


def test_case3_4():
    three_by_three = input_to_array("@.@\n.@.\n@.@")
    three_by_three_step1 = count_neighbors(three_by_three)
    print(three_by_three_step1)
    print("----")
    three_by_three_step1[three_by_three_step1 == 0] = 7
    print(three_by_three_step1)
    print("----")
    three_by_three_step1[three_by_three_step1 <= 5] = 1
    print(three_by_three_step1)
    print("----")
    three_by_three_step1[three_by_three_step1 != 1] = 0
    print(three_by_three_step1)
