from z3 import *
from quadratic_solver2 import *


def test_quadratic_solver():
    # Define symbolic inputs
    a = Real('a')
    b = Real('b')
    c = Real('c')

    # Define tactic to explore all cases
    tactic_solver = Then(
        Repeat(OrElse(Tactic('split-clause'), Tactic('skip'))),  
        Tactic('smt')
    ).solver()

    # Define constraints in a list
    constraints = [
        a == 0,  # Linear case
        And(a != 0, b * b - 4 * a * c < 0),  # Complex roots case
        And(a != 0, b * b - 4 * a * c == 0),  # Single root case
        And(a != 0, b * b - 4 * a * c > 0),  # Two distinct real roots case
        # Simulated positive and negative infinity cases
        # And(a != 0, Or(b * b - 4 * a * c == 1e308, b * b - 4 * a * c == -1e308))
        And(a != 0, b > 0, b * b - 4 * a * c == 0),  # Single root case
        And(a == 1, b == -4, c == 3),
        And(a == 5, b == 2, c == 3)
    ]


    i = 0
    while i < len(constraints):
        tactic_solver.push()  # Save current state
        tactic_solver.add(constraints[i])
       
        
        if tactic_solver.check() == sat:
            model = tactic_solver.model()
            a_val = float(model.eval(a, model_completion=True).as_decimal(5))
            b_val = float(model.eval(b, model_completion=True).as_decimal(5))
            c_val = float(model.eval(c, model_completion=True).as_decimal(5))

            try:
                roots = solve_quadratic(a_val, b_val, c_val)
                valid = validate_input(a_val, b_val, c_val, roots)
                
                # Assert that validation is True (roots satisfy the equation)
                assert valid, f"Validation failed for solve_quadratic({a_val}, {b_val}, {c_val}) with roots {roots}"
                
                print(f"Test: solve_quadratic({a_val}, {b_val}, {c_val}) => Roots: {roots}, Validation: {valid}")
            
            except LinearEquationException:
                # Assert that LinearEquationException occurs only when a == 0
                assert a_val == 0.0, f"LinearEquationException raised incorrectly for a={a_val}, b={b_val}, c={c_val}"
                print(f"Test: solve_quadratic({a_val}, {b_val}, {c_val}) => LinearEquationException")

            except NotEnoughPrecisionException:
                # Adjusted assertion: NotEnoughPrecisionException should only be raised when at least one coefficient is NaN
                assert any(math.isnan(x) for x in [a_val, b_val, c_val]), \
                    f"NotEnoughPrecisionException raised incorrectly for a={a_val}, b={b_val}, c={c_val}"
                print(f"Test: solve_quadratic({a_val}, {b_val}, {c_val}) => NotEnoughPrecisionException")

            except InfinityException:
                # Assert that InfinityException occurs when at least one coefficient is Infinity
                assert any(math.isinf(x) for x in [a_val, b_val, c_val]), \
                    f"InfinityException raised incorrectly for a={a_val}, b={b_val}, c={c_val}"
                print(f"Test: solve_quadratic({a_val}, {b_val}, {c_val}) => InfinityException")
                
        tactic_solver.pop()  # Restore previous state
        i += 1


if __name__ == "__main__":
    test_quadratic_solver()
