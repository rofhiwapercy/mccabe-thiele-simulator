#Equilibrium calculations for the McCabe-Thiele simulator
#Functions

def equilibrium_y(x, alpha):
    if not 0 <= x <= 1:
        raise ValueError("Liquid composition x must be between 0 and 1")
    if alpha <= 1:
        raise ValueError("Relative volatility alpha must be greater than 1")

    return (alpha * x) / (1 + (alpha - 1) * x)

def equilibrium_curve(alpha, points=500):
    if points < 2:
        raise ValueError("Number of points must be at least 2.")
    x_values = [
        i / (points - 1)
        for i in range(points)
    ]
    y_values = [
        equilibrium_y(x, alpha)
        for x in x_values
    ]
    return x_values, y_values