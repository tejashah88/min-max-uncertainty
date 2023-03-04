#!/usr/bin/env python3

if __name__ == "__main__":
    from minmax import MinMaxWorkspace
    from sympy import *

    space = MinMaxWorkspace()

    # add variables
    L = space.add_var('L')
    y = space.add_var('Y')
    m = space.add_var('M')
    x = space.add_var('X')

    # define and set equation
    equ = m * y / (x/L)
    space.save_equation(equ)

    # calculate and print min and max uncertainty equations
    space.display_minmax_equations()

    # evaluate min and max uncertainty equations with data
    space.calc_uncertainties({
        'L': 1886.5,
        'dL': 1.0,

        'Y': 632.8 / (10 ** 6),
        'dY': 0,
        'M': [1,2,3,4,-1,-2,-3,-4],
        'dM': 0,

        'X': [30, 61, 90, 120, -30, -60, -89, -118],
        'dX': 0.5,
    }, 4)
