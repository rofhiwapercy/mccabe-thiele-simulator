#Operating line calculations for the McCabe-Thiele simulator.
#Functions
def rectifying_line(x, xD, reflux_ratio):
    if not 0 <= xD <= 1:
        raise ValueError("Distillate composition xD must be between 0 and 1.")
    if reflux_ratio <= 0:
        raise ValueError("Reflux ratio must be greater than 0.")
    slope = reflux_ratio / (reflux_ratio + 1)
    intercept = xD / (reflux_ratio + 1)

    return slope * x + intercept

def q_line(x, zF, q):
    if not 0 <= zF <= 1:
        raise ValueError("Feed composition zF must be between 0 and 1")
    if q == 1:
        raise ValueError("For q = 1, the q-line is vertical and should be handled separately")
    slope = q / (q - 1)
    intercept = -zF / (q - 1)

    return slope * x + intercept

def q_line_x(q, zF):
    if not 0 <= zF <= 1:
        raise ValueError("Feed composition zF must be between 0 and 1")
    if q != 1:
        raise ValueError("q_line_x is only used when q = 1")

    return zF

def operating_line_intersection(xD, reflux_ratio, zF, q):
    if q == 1:
        x_intersection = zF
        y_intersection = rectifying_line(x_intersection,xD,reflux_ratio)

        return x_intersection, y_intersection

    # Top operating line:
    # y = mR*x + bR
    mR = reflux_ratio / (reflux_ratio + 1)
    bR = xD / (reflux_ratio + 1)

    # q-line:
    # y = mq*x + bq
    mq = q / (q - 1)
    bq = -zF / (q - 1)
    if mR == mq:
        raise ValueError("The rectifying operating line and q-line are parallel")
    x_intersection = (bq - bR) / (mR - mq)
    y_intersection = rectifying_line(x_intersection, xD, reflux_ratio)

    return x_intersection, y_intersection

def stripping_line(x, xB, x_intersection, y_intersection):
    if not 0 <= xB <= 1:
        raise ValueError("Bottoms composition xB must be between 0 and 1")
    if x_intersection == xB:
        raise ValueError("Cannot calculate stripping line because the two points " "have the same x-coordinate.")
    slope = (y_intersection - xB) / (x_intersection - xB)
    intercept = xB - slope * xB

    return slope * x + intercept