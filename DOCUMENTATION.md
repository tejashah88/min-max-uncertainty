# Documentation
## Table of Contents
* [Pre-requisites for MacOS/Linux](#pre-requisites-for-macoslinux)
* [Installation (for now)](#installation-for-now)
  * [Linux or MacOS](#linux-or-macos)
  * [Windows (UNTESTED)](#windows-untested)
* [How to use](#how-to-use)
  * [Adding a variable](#adding-a-variable)
  * [Adding a constant](#adding-a-constant)
  * [Saving the equation & fetching the min/max equations](#saving-the-equation--fetching-the-minmax-equations)
  * [Pretty printing the min/max equations](#pretty-printing-the-minmax-equations)
  * [Calculating uncertainty values](#calculating-uncertainty-values)

## Pre-requisites for MacOS/Linux
```bash
sudo apt-get install texlive-latex-extra dvipng
```

## Installation (for now)
### Linux or MacOS
```bash
git clone https://github.com/tejashah88/devpost-profile-exporter.git
cd devpost-profile-exporter
virtualenv env
source env/bin/activate
pip install --editable .
```

### Windows (UNTESTED)
```bat
git clone https://github.com/tejashah88/devpost-profile-exporter.git
cd devpost-profile-exporter
virtualenv env
env/bin/activate.bat
pip install --editable .
```

## How to use
### Adding a variable
```python
"""
Register an input variable with a defined uncertainty into the workspace. It
will return a Sympy variable that you can use for constructing your equation.

Parameters:
- 'name' (string) is the name of the variable. It'd recommended to put uppercase
    letters since that's how it's stored internally and it looks better when
    displaying the uncertainty variables.
- 'has_inverse_trig' (boolean) is a flag for if inverse trig functions will be
    applied so that the domain is restricted when computing the min/max equations.

Example:
    from minmax import MinMaxWorkspace
    from sympy import *

    space = MinMaxWorkspace()
    x = space.add_var('X')
    t = space.add_var('T', True)
"""
var = space.add_var(name, has_inverse_trig=False)
```

### Adding a constant
```python
"""
Register a constant into the workspace. It will return a Sympy variable that you
can use for constructing your equation.

Parameters:
- 'name' (string) is the name of the constant. It'd recommended to put uppercase
    letters since that's how it's stored internally and it looks better when displaying
    the uncertainty variables.
- 'value' (number) is the value of the constant.

Example:
    from minmax import MinMaxWorkspace
    from sympy import *

    space = MinMaxWorkspace()
    g = space.add_const('G', 9.81)
"""
const = space.add_const(name, value)
```

### Saving the equation & fetching the min/max equations
```python
"""
Saves the equation and computes the corresponding min/max equations.

Parameters:
- 'expr' (sympy expression) is the equation.
- 'simplify_equ' (boolean) is a flag, where it will allow simplifying the equation
    before calculating the min/max uncertainties.

Example:
    from minmax import MinMaxWorkspace
    from sympy import *

    space = MinMaxWorkspace()
    t = space.add_var('T')

    equ = t ** 2 + 5
    space.save_equation(equ)
    pprint(space.min_equation)
    pprint(space.min_equation)
"""
space.set_equation(expr, simplify_equ=True)
```

### Pretty printing the min/max equations
```python
"""
Pretty prints the min/max equaitons as a table.

Example:
    from minmax import MinMaxWorkspace
    from sympy import *

    space = MinMaxWorkspace()
    t = space.add_var('T')

    equ = t ** 2 + 5
    space.set_equation(equ)
    space.display_minmax_equations()
"""
space.print_minmax_equations()
```

### Calculating uncertainty values
```python
"""
Calculate error-propagated uncertainty values given raw data and uncertainties
for said data. The first argument takes a map, with the keys being variable names
or their respective uncertainty values (i.e. 'T' is to 'dT'), and the values being
either singular values or arrays.

Parameters:
- 'var_map' (string to number/array map) is the variable to values map for
    evaluating the min and max equations for the final uncertainty.
- 'dec_places' (number) is the number of decimal places to round the min, max,
    and final uncertainty values.

Example:
    from minmax import MinMaxWorkspace
    from sympy import *

    space = MinMaxWorkspace()
    t = space.add_var('T')

    equ = t ** 2 + 5
    space.set_equation(equ)
    space.calc_uncertainties({
        'T': [1.02, 2.03, 2.98, 4.05],
        'dT': 0.05
    }, 2)
"""
space.calc_uncertainties(var_map, dec_places=6)
```