from __future__ import annotations
from enum import Enum

BIT_LIMIT = 8


class BinarySearchType(Enum):
    FIXED = 0
    BUGGY = 1


class BitLimitedInteger:
    def __init__(self, value: int | BitLimitedInteger = 0, bit_limit: int = BIT_LIMIT):
        assert isinstance(value, int) or isinstance(value, BitLimitedInteger), "Only integer or BitLimitedInteger can "\
                                                                               "be used to initialise "\
                                                                               "BitLimitedInteger"
        assert isinstance(bit_limit, int), "Only integer can be used for bit_limit"
        self.bit_limit: int = bit_limit
        self.value: int = self._integer_wraparound(int(value))

    def __int__(self) -> int:
        return self._integer_wraparound(self.value)

    def __add__(self, other: int | BitLimitedInteger) -> BitLimitedInteger:
        return BitLimitedInteger(self.value + int(BitLimitedInteger(other)))

    def __sub__(self, other: int | BitLimitedInteger) -> BitLimitedInteger:
        return BitLimitedInteger(self.value - int(BitLimitedInteger(other)))

    def __mul__(self, other: int | BitLimitedInteger) -> BitLimitedInteger:
        return BitLimitedInteger(self.value * int(BitLimitedInteger(other)))

    def __floordiv__(self, other: int | BitLimitedInteger) -> BitLimitedInteger:
        return BitLimitedInteger(self.value // int(BitLimitedInteger(other)))

    def __truediv__(self, other):
        raise ArithmeticError("BitLimitedInteger does not support floating point division")

    def __mod__(self, other: int | BitLimitedInteger) -> BitLimitedInteger:
        return BitLimitedInteger(self.value % int(BitLimitedInteger(other)))

    def __lt__(self, other: int | BitLimitedInteger) -> bool:
        return self.value < int(BitLimitedInteger(other))

    def __gt__(self, other: int | BitLimitedInteger) -> bool:
        return self.value > int(BitLimitedInteger(other))

    def __eq__(self, other: int | BitLimitedInteger) -> bool:
        return self.value == int(BitLimitedInteger(other))

    def __ne__(self, other: int | BitLimitedInteger) -> bool:
        return self.value != int(BitLimitedInteger(other))

    def __le__(self, other: int | BitLimitedInteger) -> bool:
        return self.value <= int(BitLimitedInteger(other))

    def __ge__(self, other: int | BitLimitedInteger) -> bool:
        return self.value >= int(BitLimitedInteger(other))

    def __and__(self, other: int | BitLimitedInteger) -> BitLimitedInteger:
        return BitLimitedInteger(self.value & int(BitLimitedInteger(other)))

    def __or__(self, other: int | BitLimitedInteger) -> BitLimitedInteger:
        return BitLimitedInteger(self.value | int(BitLimitedInteger(other)))

    def __xor__(self, other: int | BitLimitedInteger) -> BitLimitedInteger:
        return BitLimitedInteger(self.value ^ int(BitLimitedInteger(other)))

    def __invert__(self) -> BitLimitedInteger:
        return BitLimitedInteger(~self.value)

    def _integer_wraparound(self, value: int) -> int:
        # Modified from Stack Overflow: https://stackoverflow.com/a/7771363
        if not -self._max_int() - 1 <= value <= self._max_int():
            value: int = (value + (self._max_int() + 1)) % (2 * (self._max_int() + 1)) - self._max_int() - 1
        return value

    def _max_int(self) -> int:
        return (2 ** (self.bit_limit - 1)) - 1


def overflow_binary_search(array: list[int], num: int, size_of_array: int,
                           run_type: BinarySearchType = BinarySearchType.BUGGY) -> int:
    # Source: https://www.geeksforgeeks.org/python-program-for-binary-search/
    low: BitLimitedInteger = BitLimitedInteger(0)
    high: BitLimitedInteger = BitLimitedInteger(size_of_array - 1)
    loop_count = 0
    while low <= high:
        loop_count += 1
        if run_type == BinarySearchType.BUGGY:
            # This should overflow
            mid: BitLimitedInteger = BitLimitedInteger(high + low) // 2
        else:
            # This should work
            mid: BitLimitedInteger = BitLimitedInteger(BitLimitedInteger(BitLimitedInteger(high - low) // 2) + low)
            #    ^^^                 ^^^               ^^^               ^^^     When you don't trust your own code

        print(f"Loop {loop_count}: low = {int(low)}\t high = {int(high)}\t mid = {int(mid)}")

        # If x is greater, ignore left half
        if array[int(mid)] < num:
            low = mid + 1

        # If x is smaller, ignore right half
        elif array[int(mid)] > num:
            high = mid - 1

        # means x is present at mid
        else:
            return int(mid)
        if loop_count >= size_of_array:
            print("Error: Entered a forever loop")
            break
    # If we reach here, then the element was not present
    return -1


def test():
    test_array = list(range(1, BitLimitedInteger()._max_int() - 20))  # Give my homeboy some chance to run without bug

    print()
    print("======================= Test: 1 -- Find:   7 -- Mode: BUGGY -- Expectation: Working =======================")
    print(f"Found at index = {overflow_binary_search(test_array, 7, len(test_array))}")

    print()
    print("======================= Test: 2 -- Find: 100 -- Mode: BUGGY -- Expectation: Unknown =======================")
    print(f"Found at index = {overflow_binary_search(test_array, 100, len(test_array))}")

    print()
    print("======================= Test: 3 -- Find: 100 -- Mode: FIXED -- Expectation: Working =======================")
    print(f"Found at index = {overflow_binary_search(test_array, 100, len(test_array), BinarySearchType.FIXED)}")


if __name__ == '__main__':
    test()
