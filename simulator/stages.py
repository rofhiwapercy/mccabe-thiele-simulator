#Stages calculations for the McCabe-Thiele simulator
#Imports
from .equilibrium import equilibrium_y
from .operating_lines import rectifying_line, stripping_line

#Functions
def inverse_equilibrium(y, alpha):
    if not 0 <= y <= 1:
        raise ValueError("Vapor composition y must be between 0 and 1")
    if alpha <= 1:
        raise ValueError("Relative volatility alpha must be greater than 1")
    denominator = alpha - y * (alpha - 1)
    if denominator <= 0:
        raise ValueError("Invalid equilibrium calculation")

    return y / denominator

def step_to_equilibrium(y, alpha):
    return inverse_equilibrium(y, alpha)

def step_to_operating_line(x,xD,reflux_ratio,xB,x_intersection,y_intersection,rectifying=True):
    if rectifying:
        return rectifying_line( x, xD,reflux_ratio)
    return stripping_line(x,xB, x_intersection,y_intersection)

def perform_stage_stepping(alpha,xD,xB,reflux_ratio,x_intersection,y_intersection,max_stages=100):
    if not 0 < xB < xD < 1:
        raise ValueError("Compositions must satisfy 0 < xB < xD < 1")
    if reflux_ratio <= 0:
        raise ValueError("Reflux ratio must be greater than 0")
    if max_stages < 1:
        raise ValueError("max_stages must be at least 1")
    x_current = xD
    y_current = xD

    # Store staircase coordinates.
    stage_points = [(x_current, y_current)]
    stage_number = 0
    feed_stage = None

    while x_current > xB and stage_number < max_stages:
        x_equilibrium = step_to_equilibrium(y_current, alpha)
        stage_points.append((x_equilibrium, y_current))

        # Count this theoretical stage.
        stage_number += 1

        if x_equilibrium >= x_intersection:
            rectifying = True
        else:
            rectifying = False

            if feed_stage is None:
                feed_stage = stage_number
        y_operating = step_to_operating_line(
            x_equilibrium,
            xD,
            reflux_ratio,
            xB,
            x_intersection,
            y_intersection,
            rectifying
        )

        stage_points.append(
            (x_equilibrium, y_operating)
        )

        x_current = x_equilibrium
        y_current = y_operating

    if stage_number >= max_stages and x_current > xB:
        raise RuntimeError(
            "Maximum number of stages reached before "
            "the bottoms composition was reached."
        )
    partial_stage = False
    if x_current < xB:
        partial_stage = True

    return {
        "stage_points": stage_points,
        "number_of_stages": stage_number,
        "feed_stage": feed_stage,
        "partial_stage": partial_stage
    }