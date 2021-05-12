# -*- coding: utf-8 -*-
"""
In this file your task is to write the solver function!

"""
from utils import *


# compute the membership degree using the formula for triangles
class Fuzzyfier:
    def __init__(self, left, right, mean=None):
        self._left = left
        self._right = right
        self._mean = mean

        if self._mean is None:
            self._mean = (self._left + self._right) / 2

    def compute_fuzzy_triangle(self, x):
        if self._left is not None and self._left <= x < self._mean:
            return (x - self._left) / (self._mean - self._left)
        elif self._right is not None and self._mean <= x < self._right:
            return (self._right - x) / (self._right - self._mean)
        else:
            return 0


# gives a fuzzy membership function to a given range
def functions(ranges):
    return {fuzzy_set: Fuzzyfier(*interval) for (fuzzy_set, interval) in ranges.items()}


# computes the membership for each fuzzy set based on its associated function (values between 0 and 1)
def compute_fuzzy_value(value, functions):
    return {fuzzy_set: function.compute_fuzzy_triangle(value) for (fuzzy_set, function) in functions.items()}


theta_functions = functions(theta_ranges)
omega_functions = functions(omega_ranges)


def solver(t, w):
    """
    Parameters
    ----------
    t : TYPE: float
        DESCRIPTION: the angle theta
    w : TYPE: float
        DESCRIPTION: the angular speed omega

    Returns
    -------
    F : TYPE: float
        DESCRIPTION: the force that must be applied to the cart
    or
    
    None :if we have a division by zero

    """

    theta_value = compute_fuzzy_value(t, theta_functions)  # membership degree for t
    omega_value = compute_fuzzy_value(w, omega_functions)  # membership degree for w

    degree_f = {} #membership degree of F for each set

    for theta_set in fuzzy_rules:
        for omega_set, f_set in fuzzy_rules[theta_set].items():
            # for each cell we take the minimum of the membership values
            # of the index set
            value = min(theta_value[theta_set], omega_value[omega_set])
            if f_set not in degree_f:
                degree_f[f_set] = value
            else:
                degree_f[f_set] = max(value, degree_f[f_set])

    denominator = sum(degree_f.values())
    if denominator == 0:
        return

    # defuzzify the results for F using a weighted average of the membership degrees
    # and the b values of the sets
    numerator = 0
    for f_set in degree_f.keys():
        numerator += degree_f[f_set] * vectors[f_set]

    result = numerator / denominator

    return result
