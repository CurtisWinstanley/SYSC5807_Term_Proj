import math
import cmath
from decimal import Decimal, InvalidOperation

# Exception class
class NotEnoughPrecisionException(Exception):
    pass

# Exception class
class LinearEquationException(Exception):
    pass

# Exception class
class InfinityException(Exception):
    pass



def sign(b: float) -> int:
    """Returns the sign of a number."""
    if b > 0:
        return 1 
    else:
        return -1

def sqrt_by_newton(value: float, error=1e-10) -> float:
    """Approximates square root using Newton's method."""
    if value == 0:
        return 0
    
    previous = (1 + value) / 2
    while True:
        result = (previous + value / previous) / 2
        if abs(previous - result) < error:
            break
        previous = result
    
    return result


def solve_quadratic(a: float, b: float, c: float):
    """Solves a quadratic equation ax^2 + bx + c = 0 and returns the roots."""
    if a == 0:
        raise LinearEquationException()

    discriminant = b * b - 4 * a * c
    
    # If any coefficient is NaN, raise NotEnoughPrecisionException first
    if any(math.isnan(x) for x in [a, b, c]):
        raise NotEnoughPrecisionException()
    
    # If any coefficient is Infinity, raise InfinityException
    if any(math.isinf(x) for x in [a, b, c]):
        raise InfinityException()

    if discriminant < 0:  # Complex roots
        sqrt = sqrt_by_newton(-discriminant)
        real = -b / (2 * a)
        imaginary = sqrt / (2 * a)
        return [complex(real, imaginary), complex(real, -imaginary)]

    else:  # Real roots
        sqrt = sqrt_by_newton(discriminant)
        q = -0.5 * (b + sign(b) * sqrt)
        
        x1 = q / a
        x2 = c / q if q != 0 else x1  # Avoid division by zero

        if x1 != x2:
            return [x1, x2]
        else:
            return [x1]



def is_close(a, b, tol=1e-6):
    """Helper function to compare floats and complex numbers with a tolerance."""
    return math.isclose(a.real, b.real, abs_tol=tol) and math.isclose(a.imag, b.imag, abs_tol=tol)




def validate_input(a, b, c, roots, tol=1e-6):
    """Checks if the computed roots satisfy the quadratic equation approximately."""
    
    discriminant = b * b - 4 * a * c
    
    # Determine expected number of roots
    if discriminant == 0:
        expected_root_count = 1  # One real root (double root)
    else:
        expected_root_count = 2  # Two complex roots
    
    # Check if the number of computed roots matches expectation
    if len(roots) != expected_root_count:
        return False  # Incorrect number of roots returned

    # Verify each root satisfies the equation approximately
    
    for root in roots:
        computed_value = a * root**2 + b * root + c
        if not is_close(computed_value, 0, tol):
            return False
    
    return True


