from simulator.simulation import run_simulation

def test_basic_simulation():
    results = run_simulation(
        alpha=2.5,
        xD=0.95,
        xB=0.05,
        zF=0.50,
        reflux_ratio=2.0,
        q=1.0,
    )

    assert results["number_of_stages"] > 0
    assert results["minimum_reflux"] > 0

    assert len(results["equilibrium_curve"]["x"]) > 0
    assert len(results["equilibrium_curve"]["y"]) > 0

    assert len(results["rectifying_line"]["x"]) > 0
    assert len(results["q_line"]["x"]) > 0
    assert len(results["stripping_line"]["x"]) > 0

    assert len(results["stages"]) > 0


def test_equilibrium_curve():
    results = run_simulation(
        alpha=2.5,
        xD=0.95,
        xB=0.05,
        zF=0.50,
        reflux_ratio=2.0,
        q=1.0,
    )

    x_values = results["equilibrium_curve"]["x"]
    y_values = results["equilibrium_curve"]["y"]

    assert x_values[0] == 0
    assert y_values[0] == 0

    assert x_values[-1] == 1
    assert y_values[-1] == 1


def test_invalid_reflux_ratio():
    try:
        run_simulation(
            alpha=2.5,
            xD=0.95,
            xB=0.05,
            zF=0.50,
            reflux_ratio=0.01,
            q=1.0,
        )
    except ValueError:
        return

    raise AssertionError(
        "Expected ValueError for reflux ratio below Rmin."
    )