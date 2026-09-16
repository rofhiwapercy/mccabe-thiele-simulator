# simulator/simulation.py
# Complete McCabe-Thiele simulation
#Imports
from .equilibrium import equilibrium_curve
from .operating_lines import (rectifying_line,q_line,stripping_line,)
from .calculations import ( calculate_minimum_reflux, calculate_operating_lines,calculate_rectifying_line_parameters,)
from .stages import perform_stage_stepping

#Functions
def run_simulation(alpha,xD,xB,zF,reflux_ratio,q,):
    # Validate the main inputs
    validate_inputs(alpha,xD,xB,zF,reflux_ratio,q,)

    # Calculate minimum reflux ratio
    r_min = calculate_minimum_reflux( alpha=alpha,xD=xD,zF=zF,q=q,)

    if reflux_ratio <= r_min:
        raise ValueError(
            f"Operating reflux ratio R = {reflux_ratio:.4f} "
            f"must be greater than minimum reflux ratio "
            f"Rmin = {r_min:.4f}."
        )

    # Calculate operating-line intersection

    operating_lines = calculate_operating_lines(alpha=alpha,xD=xD,xB=xB,zF=zF,reflux_ratio=reflux_ratio,q=q,)
    x_intersection = operating_lines[
        "x_intersection"
    ]
    y_intersection = operating_lines[
        "y_intersection"
    ]
    # Generate equilibrium curve

    equilibrium_x, equilibrium_y = equilibrium_curve(alpha=alpha,points=500,)
    # 6. Generate rectifying operating line
    line_x = [i / 499 for i in range(500)]
    rectifying_y = [
        rectifying_line(
            x,
            xD,
            reflux_ratio,
        )
        for x in line_x
    ]

    # Generate q-line
    q_x = []
    q_y = []
    if q == 1:
        # Vertical q-line.
        q_x = [zF, zF]
        q_y = [0, 1]
    else:
        q_x = line_x
        q_y = [
            q_line(
                x,
                zF,
                q,
            )
            for x in q_x
        ]

    # 8. Generate stripping operating line
    stripping_y = [
        stripping_line(
            x,
            xB,
            x_intersection,
            y_intersection,
        )
        for x in line_x
    ]
    #  Perform McCabe-Thiele stage stepping
    stages = perform_stage_stepping(alpha=alpha,xD=xD,xB=xB,reflux_ratio=reflux_ratio,x_intersection=x_intersection,y_intersection=y_intersection,)

    # 10. Calculate rectifying line parameters
    rectifying_parameters = (
        calculate_rectifying_line_parameters(
            xD=xD,
            reflux_ratio=reflux_ratio,
        )
    )
    # Return all results
    return {
        "inputs": {
            "alpha": alpha,
            "xD": xD,
            "xB": xB,
            "zF": zF,
            "reflux_ratio": reflux_ratio,
            "q": q,
        },

        "minimum_reflux": r_min,

        "operating_lines": {
            "x_intersection": x_intersection,
            "y_intersection": y_intersection,

            "rectifying_slope": (
                rectifying_parameters["slope"]
            ),

            "rectifying_intercept": (
                rectifying_parameters["intercept"]
            ),
        },

        "equilibrium_curve": {
            "x": equilibrium_x,
            "y": equilibrium_y,
        },

        "rectifying_line": {
            "x": line_x,
            "y": rectifying_y,
        },

        "q_line": {
            "x": q_x,
            "y": q_y,
        },

        "stripping_line": {
            "x": line_x,
            "y": stripping_y,
        },

        "stages": stages["stage_points"],

        "number_of_stages": (
            stages["number_of_stages"]
        ),

        "feed_stage": (
            stages["feed_stage"]
        ),

        "partial_stage": (
            stages["partial_stage"]
        ),
    }


def validate_inputs(alpha,xD,xB,zF,reflux_ratio, q,):
    if alpha <= 1:
        raise ValueError(
            "Relative volatility alpha must be greater than 1."
        )
    if not 0 < xB < 1:
        raise ValueError("Bottoms composition xB must be between 0 and 1")
    if not 0 < xD < 1:
        raise ValueError("Distillate composition xD must be between 0 and 1")
    if not 0 <= zF <= 1:
        raise ValueError("Feed composition zF must be between 0 and 1")
    if not xB < xD:
        raise ValueError(
            "Bottoms composition xB must be less than "
            "distillate composition xD"
        )
    if not 0 < reflux_ratio:
        raise ValueError("Reflux ratio must be greater than 0")
    if q < 0:
        raise ValueError("Feed condition q cannot be negative")