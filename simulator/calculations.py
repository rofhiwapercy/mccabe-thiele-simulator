#Calculations for the McCabe-Thiele simulator.
#Imports
from .equilibrium import equilibrium_y
from .operating_lines import ( rectifying_line, operating_line_intersection)

def calculate_minimum_reflux(alpha,xD,zF,q):
    if alpha <= 1:
        raise ValueError("Relative volatility alpha must be greater than 1")
    if not 0 <= xD <= 1:
        raise ValueError("Distillate composition xD must be between 0 and 1.")
    if not 0 <= zF <= 1:
        raise ValueError("Feed composition zF must be between 0 and 1")
    if q == 1:
        x_pinch = zF
        y_pinch = equilibrium_y(x_pinch,alpha)
    else:
        x_pinch = find_q_equilibrium_intersection( alpha, zF,q)
        y_pinch = equilibrium_y(x_pinch,alpha)
    denominator = xD - x_pinch
    if denominator <= 0:
        raise ValueError(
            "Invalid feed/distillate compositions for "
            "minimum reflux calculation."
        )
    difference = y_pinch - x_pinch
    if difference <= 0:
        raise ValueError(
            "Unable to calculate a positive minimum reflux ratio."
        )
    r_min = (xD - y_pinch) / difference
    return r_min

def find_q_equilibrium_intersection(alpha, zF,q,points=10000):
    if q == 1:
        return zF
    if points < 2:
        raise ValueError(
            "points must be at least 2."
        )
    x_previous = 0.0
    equilibrium_previous = equilibrium_y(
        x_previous,
        alpha
    )

    q_previous = (
        q / (q - 1)
    ) * x_previous - zF / (q - 1)

    difference_previous = (
        equilibrium_previous - q_previous
    )

    for i in range(1, points):

        x_current = i / (points - 1)

        equilibrium_current = equilibrium_y(
            x_current,
            alpha
        )

        q_current = (
            q / (q - 1)
        ) * x_current - zF / (q - 1)

        difference_current = (
            equilibrium_current - q_current
        )
        if (
            difference_previous == 0
            or difference_previous * difference_current < 0
        ):
            denominator = (
                difference_current
                - difference_previous
            )
            if denominator == 0:
                return x_current
            fraction = (
                -difference_previous
                / denominator
            )
            return (
                x_previous
                + fraction
                * (x_current - x_previous)
            )
        x_previous = x_current
        difference_previous = difference_current
    raise ValueError(
        "Could not find an intersection between "
        "the q-line and equilibrium curve."
    )

def calculate_operating_lines(alpha, xD,xB, zF,reflux_ratio,q):
    if not 0 < xB < xD < 1:
        raise ValueError(
            "Compositions must satisfy 0 < xB < xD < 1."
        )

    if not 0 <= zF <= 1:
        raise ValueError(
            "Feed composition zF must be between 0 and 1."
        )

    if reflux_ratio <= 0:
        raise ValueError(
            "Reflux ratio must be greater than 0."
        )

    x_intersection, y_intersection = (
        operating_line_intersection(
            xD,
            reflux_ratio,
            zF,
            q
        )
    )

    return {
        "x_intersection": x_intersection,
        "y_intersection": y_intersection,
    }


def calculate_rectifying_line_parameters(xD,reflux_ratio):
    if reflux_ratio <= 0:
        raise ValueError("Reflux ratio must be greater than 0")
    slope = reflux_ratio / (reflux_ratio + 1)
    intercept = xD / (reflux_ratio + 1)

    return {
        "slope": slope,
        "intercept": intercept,
    }