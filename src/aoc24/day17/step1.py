from enum import IntEnum
from typing import Any


class Operation(IntEnum):
    ADV = 0  # A = A / 2^O
    BXL = 1  # B = B ^ O
    BST = 2  # B = O % 8
    JNZ = 3  # if A != 0, jump to O
    BXC = 4  # B = B ^ C
    OUT = 5  # O % *
    BDV = 6  #
    CDV = 7  #


class CPU:
    reg_A: int
    reg_B: int
    reg_C: int
    reg_PC: int
    output: list[int]

    def __init__(self, reg_A: int, reg_B: int, reg_C: int, *args: Any, **kwds: Any):
        self.reg_A = reg_A
        self.reg_B = reg_B
        self.reg_C = reg_C
        self.reg_PC = 0
        self.output = []

    def operate(self, op: int | Operation, literal_operand: int):
        op = op if isinstance(op, Operation) else Operation(op)

        if op == Operation.ADV:
            self.reg_A = self.reg_A // (2 ** self.__get_combo_operand(literal_operand))
        elif op == Operation.BXL:
            self.reg_B = self.reg_B ^ literal_operand
        elif op == Operation.BST:
            self.reg_B = self.__get_combo_operand(literal_operand) % 8
        elif op == Operation.JNZ:
            if self.reg_A != 0:
                self.reg_PC = literal_operand
        elif op == Operation.BXC:
            self.reg_B = self.reg_B ^ self.reg_C
        elif op == Operation.OUT:
            self.output.append(self.__get_combo_operand(literal_operand) % 8)
        elif op == Operation.BDV:
            self.reg_B = self.reg_A // (2 ** self.__get_combo_operand(literal_operand))
        elif op == Operation.CDV:
            self.reg_C = self.reg_A // (2 ** self.__get_combo_operand(literal_operand))
        else:
            raise ValueError(f"Unknown operation {op}")

    def __get_combo_operand(self, literal_operand: int) -> int:
        if 0 <= literal_operand <= 3:
            return literal_operand
        elif literal_operand == 4:
            return self.reg_A
        elif literal_operand == 5:
            return self.reg_B
        elif literal_operand == 6:
            return self.reg_C
        else:
            raise ValueError(f"Invalid operand {literal_operand}")

    def run_program(self, program: list[int], debug=False):
        while self.reg_PC < len(program):
            op = program[self.reg_PC]
            operand = program[self.reg_PC + 1]
            self.reg_PC += 2

            if debug:
                print(Operation(op).name, operand)
                print(self)
            self.operate(op, operand)
            if debug:
                print(self)
                input()

    def __repr__(self) -> str:
        return f"A={self.reg_A}({bin(self.reg_A)}), B={self.reg_B}, C={self.reg_C}, PC={self.reg_PC}"


def test():
    cpu = CPU(0, 0, 9)
    cpu.run_program([2, 6])
    assert cpu.reg_B == 1

    cpu = CPU(10, 0, 0)
    cpu.run_program([5, 0, 5, 1, 5, 4])
    assert cpu.output == [0, 1, 2]

    cpu = CPU(2024, 0, 0)
    cpu.run_program([0, 1, 5, 4, 3, 0])
    assert cpu.output == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0], cpu.output
    assert cpu.reg_A == 0

    cpu = CPU(0, 29, 0)
    cpu.run_program([1, 7])
    assert cpu.reg_B == 26

    cpu = CPU(0, 2024, 43690)
    cpu.run_program([4, 0])
    assert cpu.reg_B == 44354

    cpu = CPU(729, 0, 0)
    program = [0, 1, 5, 4, 3, 0]
    cpu.run_program(program)
    assert cpu.output == [4, 6, 3, 5, 6, 3, 5, 2, 1, 0]
    assert ",".join(str(x) for x in cpu.output) == "4,6,3,5,6,3,5,2,1,0"


def main():
    cpu = CPU(22571680, 0, 0)
    cpu.run_program([2, 4, 1, 3, 7, 5, 0, 3, 4, 3, 1, 5, 5, 5, 3, 0])
    assert cpu.output != [6, 2, 4, 3, 0, 6, 0, 4, 7]
    assert cpu.output == [2, 0, 1, 3, 4, 0, 2, 1, 7]

    # B = A % 8 (2, 4)
    # B = B ^ 3 (1, 3)
    # C = A / 2 ** B (7, 5)
    # A = A / 2 ** 3 (0, 3)
    # B = B ^ C (4, 3)
    # B = B ^ 5 (1, 5)
    # out(B % 8) (5, 5)

    for i in range(2048):
        cpu = CPU(i, 0, 0)
        cpu.run_program([2, 4, 1, 3, 7, 5, 0, 3, 4, 3, 1, 5, 5, 5])

        print(f"{i: 5} {i % 8} { (i // 8 )% 8} {cpu.output[0]}")

    print(",".join(str(x) for x in cpu.output))


if __name__ == "__main__":
    test()
    main()
