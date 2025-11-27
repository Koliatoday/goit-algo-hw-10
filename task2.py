"""
Monte Carlo Integration Module

This module implements Monte Carlo method for numerical integration
and compares the results with scipy's quad function.
"""

import random
import numpy as np
import scipy.integrate as spi
import matplotlib.pyplot as plt


DEFAULT_POINTS = 1000


def func_to_test(x):
    """
    Test function for integration: f(x) = sqrt(x)
    """
    return x**0.5


def integral_mc(xmax, ymax, func, points_number=DEFAULT_POINTS, seed=None):
    """
    Calculate definite integral using Monte Carlo method.

    The method generates random points in a rectangle [0, xmax] × [0, ymax]
    and counts how many points fall under the curve y = func(x).

    Args:
        xmax (float): Upper bound of integration interval [0, xmax]
        ymax (float): Maximum y-value for the bounding rectangle
        func (callable): Function to integrate, must accept a single
                        numeric argument
        points_number (int): Number of random points (default: 1000)
        seed (int, optional): Random seed for reproducibility

    Returns:
        float: Approximation of the definite integral
    """
    if points_number < 0 or not isinstance(points_number, int):
        raise ValueError("points_number must be a positive integer")

    if seed is not None:
        random.seed(seed)

    # Count points under curve (memory efficient)
    points_under_curve = sum(
        1 for _ in range(points_number)
        if random.uniform(0, ymax) <= func(random.uniform(0, xmax))
    )

    rectangle_area = xmax * ymax
    return (points_under_curve / points_number) * rectangle_area


def usage_example(xmax, points_number, func):
    """
    Demonstrate Monte Carlo integration and compare with analytical result.

    This function calculates the integral using both Monte Carlo method and
    scipy's quad function, prints the comparison, and visualizes the function
    with the integration area highlighted.

    Args:
        xmax (float): Upper bound of integration interval [0, xmax]
        func (callable): Function to integrate
    """
    if xmax < 0 or not isinstance(xmax, (int, float)):
        print("xmax must be a positive number")
        return

    analytical_result, _ = spi.quad(func, 0, xmax)
    monte_carlo_result = integral_mc(xmax, func(xmax), func, points_number)
    difference_percent = (
        abs(analytical_result - monte_carlo_result) / analytical_result * 100
    )

    print(f"Square calculated with Monte Carlo method = "
          f"{monte_carlo_result:.4f}")
    print(f"Square calculated by integral = {analytical_result:.4f}")
    print(f"Difference = {difference_percent:.4f} %")

    # Plot the graph
    x = np.linspace(0, xmax + 1, 100)
    y = func(x)
    _, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y, 'r', linewidth=2, label='f(x) = √x')

    ix = np.linspace(0, xmax)
    iy = func(ix)
    ax.fill_between(ix, iy, color='gray', alpha=0.3,
                    label='Integration area')
    ax.set_xlim([x[0], x[-1]])
    ax.set_ylim([0, max(y) + 0.1])
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.axvline(x=0, color='gray', linestyle='--')
    ax.axvline(x=xmax, color='gray', linestyle='--')
    ax.set_title(f'Integration of f(x) from 0 to {xmax}')
    ax.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    usage_example(5.55, 1000, func_to_test)
