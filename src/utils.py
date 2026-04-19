"""Mathematical utility functions module.

This module provides common mathematical operations including factorial calculation,
prime number checking, greatest common divisor, least common multiple, and
Fibonacci sequence generation.
"""

import math
from typing import List


def factorial(n: int) -> int:
    """Calculate the factorial of a non-negative integer.

    Args:
        n (int): Non-negative integer to calculate factorial for.

    Returns:
        int: Factorial of n (n!).

    Raises:
        ValueError: If n is negative.
        TypeError: If n is not an integer.
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    return math.factorial(n)


def is_prime(n: int) -> bool:
    """Check if a number is prime.

    Args:
        n (int): Integer to check for primality.

    Returns:
        bool: True if n is prime, False otherwise.

    Raises:
        TypeError: If n is not an integer.
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Check odd divisors up to sqrt(n)
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def gcd(a: int, b: int) -> int:
    """Find the greatest common divisor of two integers using Euclidean algorithm.

    Args:
        a (int): First integer.
        b (int): Second integer.

    Returns:
        int: Greatest common divisor of a and b.

    Raises:
        TypeError: If a or b is not an integer.
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Both inputs must be integers")
    return math.gcd(abs(a), abs(b))


def lcm(a: int, b: int) -> int:
    """Calculate the least common multiple of two integers.

    Args:
        a (int): First integer.
        b (int): Second integer.

    Returns:
        int: Least common multiple of a and b.

    Raises:
        TypeError: If a or b is not an integer.
        ValueError: If both a and b are zero.
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Both inputs must be integers")
    if a == 0 and b == 0:
        raise ValueError("LCM is undefined when both numbers are zero")
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def fibonacci_sequence(n: int) -> List[int]:
    """Generate the first n numbers in the Fibonacci sequence.

    Args:
        n (int): Number of Fibonacci numbers to generate.

    Returns:
        List[int]: List containing the first n Fibonacci numbers.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is negative.
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    if n < 0:
        raise ValueError("Number of terms cannot be negative")
    if n == 0:
        return []
    if n == 1:
        return [0]
    if n == 2:
        return [0, 1]

    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[i-1] + sequence[i-2])

    return sequence
