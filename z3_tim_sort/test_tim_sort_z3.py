from z3 import *
from Tim_sort import *
import random

def test_tim_sort_with_z3():
    array_len = 25
    # possible runs
    small_run = 1
    medium_run = 2
    large_run = 10
    # Create symbolic integer variables
    symbols = [Int(f'x{i}') for i in range(array_len)]
    run_size = Int("run_size")
    arr_size = Int("arr_size")
    # Define a Z3 solver
    solver = Solver()
    # Constrain values to 1-100
    for sym in symbols:
        solver.add(sym > 0, sym <= 100)
    # List of grouped constraint sets (each test case is a list of constraints)
    constraint_set = [
        [symbols[0] == symbols[1], run_size <= 0, arr_size == array_len],
        [symbols[0] > symbols[1], run_size > large_run, arr_size == array_len],
        [symbols[2] < symbols[3], run_size == small_run, arr_size == array_len],
        [symbols[2] < symbols[3], run_size == medium_run, arr_size == array_len + 1],
        [And([symbols[i] == random.randint(1, 100) for i in range(array_len)]), run_size == int(array_len/2), arr_size == array_len],
        [And([symbols[i] == 4 for i in range(array_len)]), run_size >= medium_run, run_size <= 10, arr_size == array_len],
    ]

    # Run each grouped constraint set
    for i, constraints in enumerate(constraint_set):
        solver.push()
        solver.add(*constraints)

        print(f"\nTest case {i + 1}:")
        if solver.check() == sat:
            model = solver.model()
            arr = [model.eval(sym).as_long() for sym in symbols]
            run_size_val = model.eval(run_size).as_long()
            arr_size_val = model.eval(arr_size).as_long()


            try:
                # Run timSort with valid run size
                sorted_arr = timSort(arr.copy(), arr_size_val, run_size_val)
                expected = sorted(arr)

                print(f"Expected Output: {expected}")
                assert sorted_arr == expected, f"TimSort failed on input {arr}"
            except InvalidArrayLengthException:
                print("Caught exception: InvalidArrayLengthException")
                assert True
            except InvalidRunException:
                print(f"Caught InvalidRunException as expected for run_size = {run_size_val}")
                assert run_size_val <= 0
            except Exception as e:
                print(f"Unexpected error: {e}")
                assert False

        solver.pop()


if __name__ == "__main__":
    test_tim_sort_with_z3()
