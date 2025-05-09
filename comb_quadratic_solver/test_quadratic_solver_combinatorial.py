
from quadratic_solver2 import *
from allpairspy import AllPairs
import math



def test_quadratic_solver():
    # Define test parameters for (a, b, c)
    parameters = {
        "a": [0, 1, -1, 100, -100, float('nan'), float('inf')],   # Introduce NaN for testing
        "b": [0, 1, -1, 100, -100, float('nan'), float('inf')],   # Include infinity to force undefined operations
        "c": [0, 1, -1, 100, -100, float('nan'), float('inf')]    # Include -infinity for similar reasons
    }

    # Generate pairwise (2-way) test cases --- UNCOMMENT to generate tests
    # pairwise_tests = list(AllPairs(parameters.values()))



    # Test cases generated by AllPairsPy
    test_cases = [
        [0, 0, 0], [1, 1, 0], [-1, -1, 0], [100, 100, 0], [-100, -100, 0], [float('nan'), float('nan'), 0],
        [float('inf'), float('inf'), 0], [float('inf'), float('nan'), 1], [float('nan'), -100, 1], [-100, 100, 1],
        [100, -1, 1], [-1, 1, 1], [1, 0, 1], [0, float('inf'), 1], [0, float('nan'), -1], [1, -100, -1],
        [-1, 100, -1], [100, float('inf'), -1], [-100, 0, -1], [float('nan'), 1, -1], [float('inf'), -1, -1],
        [float('inf'), 1, 100], [float('nan'), 0, 100], [-100, -1, 100], [100, float('nan'), 100], [-1, -100, 100],
        [1, float('inf'), 100], [0, 100, 100], [0, -1, -100], [1, 100, -100], [-1, float('nan'), -100], [100, 0, -100],
        [-100, 1, -100], [float('nan'), float('inf'), -100], [float('inf'), -100, -100], [float('inf'), 100, float('nan')],
        [float('nan'), -1, float('nan')], [-100, float('inf'), float('nan')], [100, -100, float('nan')],
        [-1, 0, float('nan')], [1, float('nan'), float('nan')], [0, 1, float('nan')], [0, -100, float('inf')],
        [1, -1, float('inf')], [-1, float('inf'), float('inf')], [100, 1, float('inf')], [-100, float('nan'), float('inf')],
        [float('nan'), 100, float('inf')], [float('inf'), 0, float('inf')], [1, 2, 1]
    ]


    print("\nPairwise (2-Way) Testing Results:")
    for test_case in test_cases:
        a, b, c = test_case
        try:
            roots = solve_quadratic(a, b, c)
            valid = validate_input(a, b, c, roots)
            
            # Assert that validation is True (roots satisfy the equation)
            assert valid, f"Validation failed for solve_quadratic({a}, {b}, {c}) with roots {roots}"
            
            print(f"Test: solve_quadratic({a}, {b}, {c}) => Roots: {roots}, Validation: {valid}")
        
        except LinearEquationException:
            # Assert that LinearEquationException occurs only when a == 0
            assert a == 0, f"LinearEquationException raised incorrectly for a={a}, b={b}, c={c}"
            print(f"Test: solve_quadratic({a}, {b}, {c}) => LinearEquationException")

        except NotEnoughPrecisionException:
            # Adjusted assertion: NotEnoughPrecisionException should only be raised when at least one coefficient is NaN
            assert any(math.isnan(x) for x in [a, b, c]), \
                f"NotEnoughPrecisionException raised incorrectly for a={a}, b={b}, c={c}"
            print(f"Test: solve_quadratic({a}, {b}, {c}) => NotEnoughPrecisionException")

        except InfinityException:
            # Assert that InfinityException occurs when at least one coefficient is Infinity
            assert any(math.isinf(x) for x in [a, b, c]), \
                f"InfinityException raised incorrectly for a={a}, b={b}, c={c}"
            print(f"Test: solve_quadratic({a}, {b}, {c}) => InfinityException")




if __name__ == "__main__":
    test_quadratic_solver()