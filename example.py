#!/usr/bin/env python3

if __name__ == "__main__":
    from minmax import MinMaxWorkspace
    from sympy import *

    space = MinMaxWorkspace()

    # add variables
    m = space.add_var('M')
    T = space.add_var('T')

    # define and set equation
    equ = (4*pi**2) * m / T**2
    space.save_equation(equ)

    # calculate and print min and max uncertainty equations
    space.display_minmax_equations()

    # evaluate min and max uncertainty equations with data
    space.calc_uncertainties({
        'M': [0.1995, 0.2494, 0.2994, 0.3492, 0.3995, 0.4493, 0.5002, 0.5500, 0.5599],
        'T': [0.58  , 0.64  , 0.69  , 0.74  , 0.80  , 0.84  , 0.89  , 0.95  , 0.99  ],
        'dM': 0.0002,
        'dT': 0.03
    }, 2)