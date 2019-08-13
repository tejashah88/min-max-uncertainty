import random
from sympy import symbols, simplify, pretty, N
from terminaltables import DoubleTable as FancyTable

flatten = lambda lst: [item for sublist in lst for item in sublist]

def transpose(array_2d):
    transposed = []
    rows = len(array_2d)
    cols = len(array_2d[0])

    for j in range(cols):
        row = []
        for i in range(rows):
            row.append(array_2d[i][j])
        transposed.append(row)
    return transposed

class MinMaxWorkspace:
    def __init__(self):
        self._symbols = {}
        self._equation = None
        self._min_equ = None
        self._max_equ = None

    @property
    def _has_equations(self):
        return (self.equation is not None) and (self.min_equation is not None) and (self.max_equation is not None)

    @property
    def _present_symbols(self):
        return [symbol for symbol in self._symbols.values() if self.equation.has(symbol['var'])]

    @property
    def _present_variables(self):
        return [symbol for symbol in self._present_symbols if symbol['type'] == 'variable']

    @property
    def _present_constants(self):
        return [symbol for symbol in self._present_symbols if symbol['type'] == 'constant']

    @property
    def equation(self):
        return self._equation

    @property
    def min_equation(self):
        return self._min_equ

    @property
    def max_equation(self):
        return self._max_equ

    def add_var(self, name, has_inverse_trig=False):
        name = name.upper()
        var, dvar = symbols(f'{name} d{name}')

        self._symbols[name] = {
            'type': 'variable',
            'var': var, 'dvar': dvar,
            'val': None, 'dval': None,
            'test_val': random.uniform(0, 100) if not has_inverse_trig else random.uniform(-.5, .5),
            'test_dval': random.uniform(0, 1) if not has_inverse_trig else random.uniform(-.5, .5)
        }

        return var

    def add_const(self, name, value):
        name = name.upper()
        var = symbols(name)

        self._symbols[name] = {
            'type': 'constant',
            'var': var, 'val': value
        }

        return var

    def save_equation(self, expr, simplify_equ=True):
        self._equation = simplify(expr) if simplify_equ else expr
        self._compute_minmax_equations()

    def _compute_minmax_equations(self):
        possible_exprs = [self.equation]
        max_predicted_vars = len(self._present_variables) * 2 + len(self._present_constants)

        # recursively process all variables by creating a flattened tree
        # i.e. for each unprocessed variable in an expression, make two duplicates with +/- dvar and add to possible expressions
        for xexpr in possible_exprs:
            for var in self._present_variables:
                if not xexpr.has(var['var'] + var['dvar']) and not xexpr.has(var['var'] - var['dvar']):
                    possible_exprs.append(xexpr.subs(var['var'], var['var'] + var['dvar']))
                    possible_exprs.append(xexpr.subs(var['var'], var['var'] - var['dvar']))

        # filter any expressions with unprocessed variables
        possible_exprs = [xexpr for xexpr in possible_exprs if len(xexpr.free_symbols) == max_predicted_vars]
        possible_exprs = list(set(possible_exprs))

        # figure out which equations yield the lowest and highest values with uncertainties from the original value
        possible_values = []
        for xexpr in possible_exprs:
            for var in self._present_variables:
                xexpr = xexpr.subs(var['var'], var['test_val'])
                xexpr = xexpr.subs(var['dvar'], var['test_dval'])
            for var in self._present_constants:
                xexpr = xexpr.subs(var['var'], var['val'])
            possible_values.append(xexpr)

        vmin = min(possible_values)
        imin = possible_values.index(vmin)

        vmax = max(possible_values)
        imax = possible_values.index(vmax)

        min_expr = possible_exprs[imin]
        max_expr = possible_exprs[imax]

        self._min_equ = min_expr
        self._max_equ = max_expr

    def display_minmax_equations(self):
        if not self._has_equations:
            raise Exception('Equation has not been saved!')

        data = [
            ['Equation', 'Min equation', 'Max Equation'],
            [pretty(self.equation), pretty(self.min_equation), pretty(self.max_equation)]
        ]

        print(FancyTable(data).table)

    def calc_uncertainties(self, var_map, dec_places=6):
        variables = list(var_map.keys())
        values = list(var_map.values())

        # ensure that any singular values in variable map are 1 element arrays
        for i in range(len(values)):
            if type(values[i]) != list:
                values[i] = [values[i]]

        # only look at variables whose number of values was greater than 1
        num_vars = len(variables)
        num_values = list(set(len(value) for value in values if len(value) > 1))

        if len(num_values) > 1:
            raise Exception('Dimensions of specified values do not match')

        # for all 1 element arrays, expand to the max size of the largest value array
        for i in range(len(values)):
            if len(values[i]) == 1:
                values[i] = list(values[i]) * num_values[0]

        # we go through the data row by row
        value_group = transpose(values)

        # prep the data table for displaying
        data_table = [[*variables, 'min', 'max', 'final']]

        for value_row in value_group:
            min_equ = self.min_equation
            max_equ = self.max_equation

            # substitute input variables and respective uncertainties with given values
            for i in range(num_vars):
                var = variables[i]
                val = value_row[i]
                min_equ = min_equ.subs(var, val)
                max_equ = max_equ.subs(var, val)

            # substitute constant values
            for symbol in self._present_constants:
                min_equ = min_equ.subs(symbol['var'], symbol['val'])
                max_equ = max_equ.subs(symbol['var'], symbol['val'])

            # process any known mathematical constants
            min_val = N(min_equ)
            max_val = N(max_equ)
            final_uncertainty = (max_val - min_val) / 2

            # add variable values to data table
            uncertainty_row = [round(min_val, dec_places), round(max_val, dec_places), round(final_uncertainty, dec_places)]
            data_row = [*value_row, *uncertainty_row]
            data_table += [data_row]

        print(FancyTable(data_table).table)