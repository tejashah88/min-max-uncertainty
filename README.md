# min-max-uncertainty
A min/max uncertainty calculator and data cruncher python library, mainly used for my physics labs.

## Documentation
See the [docs](DOCUMENTATION.md) for using this library as well as [example.py](example.py).

## Example
```python
from minmax import MinMaxWorkspace
from sympy import *

space = MinMaxWorkspace()

# add variables
m = space.add_var('M')
T = space.add_var('T')

# define and set equation
equ = (4*pi**2) * m / T**2
space.set_equation(equ)

# calculate and print min and max uncertainty equations
min_equ, max_equ = space.compute_minmax_equations()
space.print_minmax_equations()

# evaluate min and max uncertainty equations with data
space.calc_uncertainties({
    'M': [0.1995, 0.2494, 0.2994, 0.3492, 0.3995, 0.4493, 0.5002, 0.5500, 0.5599],
    'T': [0.58  , 0.64  , 0.69  , 0.74  , 0.80  , 0.84  , 0.89  , 0.95  , 0.99  ],
    'dM': 0.0002,
    'dT': 0.03
}, 2)
```

### Output
```bash
┌──────────┬───────────────┬───────────────┐
│ Equation │ Min equation  │ Max Equation  │
├──────────┼───────────────┼───────────────┤
│    2     │    2          │    2          │
│ 4⋅π ⋅M   │ 4⋅π ⋅(M - dM) │ 4⋅π ⋅(M + dM) │
│ ──────   │ ───────────── │ ───────────── │
│    2     │           2   │           2   │
│   T      │   (T + dT)    │   (T - dT)    │
└──────────┴───────────────┴───────────────┘
┌────────┬──────┬────────┬──────┬───────┬───────┬───────┐
│ M      │ T    │ dM     │ dT   │ min   │ max   │ final │
├────────┼──────┼────────┼──────┼───────┼───────┼───────┤
│ 0.1995 │ 0.58 │ 0.0002 │ 0.03 │ 21.14 │ 26.06 │ 2.46  │
│ 0.2494 │ 0.64 │ 0.0002 │ 0.03 │ 21.92 │ 26.48 │ 2.28  │
│ 0.2994 │ 0.69 │ 0.0002 │ 0.03 │ 22.79 │ 27.15 │ 2.18  │
│ 0.3492 │ 0.74 │ 0.0002 │ 0.03 │ 23.24 │ 27.36 │ 2.06  │
│ 0.3995 │ 0.8  │ 0.0002 │ 0.03 │ 22.88 │ 26.61 │ 1.87  │
│ 0.4493 │ 0.84 │ 0.0002 │ 0.03 │ 23.42 │ 27.05 │ 1.81  │
│ 0.5002 │ 0.89 │ 0.0002 │ 0.03 │ 23.32 │ 26.71 │ 1.69  │
│ 0.55   │ 0.95 │ 0.0002 │ 0.03 │ 22.6  │ 25.66 │ 1.53  │
│ 0.5599 │ 0.99 │ 0.0002 │ 0.03 │ 21.24 │ 23.99 │ 1.38  │
└────────┴──────┴────────┴──────┴───────┴───────┴───────┘
```

