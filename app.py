#Imports
import streamlit as st
import matplotlib.pyplot as plt
from simulator.simulation import run_simulation

# Page configuration
st.set_page_config(
    page_title="McCabe-Thiele Simulator",
    page_icon="⚗️",
    layout="wide",
)

# Title
st.title("McCabe-Thiele Distillation Simulator")

st.write(
    "Calculate and visualize theoretical stages for a binary "
    "distillation column using the McCabe-Thiele method."
)

# Sidebar inputs
st.sidebar.header("Simulation Inputs")
alpha = st.sidebar.number_input(
    "Relative volatility (α)",
    min_value=1.01,
    max_value=20.0,
    value=2.5,
    step=0.1,
)

xD = st.sidebar.number_input(
    "Distillate composition (xD)",
    min_value=0.01,
    max_value=0.99,
    value=0.95,
    step=0.01,
)

xB = st.sidebar.number_input(
    "Bottoms composition (xB)",
    min_value=0.01,
    max_value=0.99,
    value=0.05,
    step=0.01,
)

zF = st.sidebar.number_input(
    "Feed composition (zF)",
    min_value=0.0,
    max_value=1.0,
    value=0.50,
    step=0.01,
)

reflux_ratio = st.sidebar.number_input(
    "Reflux ratio (R)",
    min_value=0.01,
    max_value=20.0,
    value=2.0,
    step=0.1,
)

q = st.sidebar.number_input(
    "Feed condition (q)",
    min_value=0.0,
    max_value=2.0,
    value=1.0,
    step=0.1,
)


run_button = st.sidebar.button(
    "Run Simulation",
    type="primary",
)

# Simulation
if run_button:

    try:

        results = run_simulation(
            alpha=alpha,
            xD=xD,
            xB=xB,
            zF=zF,
            reflux_ratio=reflux_ratio,
            q=q,
        )

        st.success("Simulation completed successfully.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Theoretical Stages",
                results["number_of_stages"],
            )

        with col2:
            st.metric(
                "Minimum Reflux Ratio",
                f"{results['minimum_reflux']:.3f}",
            )

        with col3:

            if results["feed_stage"] is None:
                feed_stage = "N/A"
            else:
                feed_stage = results["feed_stage"]

            st.metric(
                "Feed Stage",
                feed_stage,
            )
        
        #McCabe-Thiele Diagram
        st.subheader("McCabe-Thiele Diagram")

        fig, ax = plt.subplots(
            figsize=(8, 8)
        )

        # Equilibrium curve
        ax.plot(
            results["equilibrium_curve"]["x"],
            results["equilibrium_curve"]["y"],
            label="Equilibrium Curve",
            linewidth=2,
        )

        # Diagonal
        ax.plot(
            [0, 1],
            [0, 1],
            linestyle="--",
            label="y = x",
            linewidth=1.2,
        )

        # Rectifying operating line
        ax.plot(
            results["rectifying_line"]["x"],
            results["rectifying_line"]["y"],
            label="Rectifying Line",
            linewidth=2,
        )

        # q-line
        ax.plot(
            results["q_line"]["x"],
            results["q_line"]["y"],
            label="q-line",
            linewidth=1.5,
        )

        # Stripping operating line
        ax.plot(
            results["stripping_line"]["x"],
            results["stripping_line"]["y"],
            label="Stripping Line",
            linewidth=2,
        )

        # Stage staircase
        stage_points = results["stages"]
        stage_x = [
            point[0]
            for point in stage_points
        ]
        stage_y = [
            point[1]
            for point in stage_points
        ]

        ax.plot(
            stage_x,
            stage_y,
            linewidth=1.8,
            marker="o",
            markersize=3,
            label="Stage Stepping",
        )

        # Distillate and bottoms composition markers
        ax.axvline(
            xD,
            linestyle=":",
            linewidth=1,
            label="xD",
        )

        ax.axvline(
            xB,
            linestyle=":",
            linewidth=1,
            label="xB",
        )

        # Feed composition marker
        ax.axvline(
            zF,
            linestyle=":",
            linewidth=1,
            label="zF",
        )

        # Intersection point
        x_intersection = results["operating_lines"][
            "x_intersection"
        ]

        y_intersection = results["operating_lines"][
            "y_intersection"
        ]

        ax.plot(
            x_intersection,
            y_intersection,
            marker="o",
            markersize=6,
            label="Operating-line intersection",
        )

        # Graph formatting
        ax.set_xlabel(
            "Liquid composition, x"
        )

        ax.set_ylabel(
            "Vapor composition, y"
        )

        ax.set_title(
            "McCabe-Thiele Diagram"
        )

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        ax.set_aspect(
            "equal",
            adjustable="box",
        )

        ax.grid(
            True,
            alpha=0.3,
        )

        ax.legend(
            loc="center left",
            bbox_to_anchor=(1, 0.5),
        )

        fig.tight_layout()

        st.pyplot(fig)

        # Operating-line information
        st.subheader("Operating Line Information")

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                "Rectifying line slope:",
                f"{results['operating_lines']['rectifying_slope']:.4f}",
            )

            st.write(
                "Rectifying line intercept:",
                f"{results['operating_lines']['rectifying_intercept']:.4f}",
            )

        with col2:

            st.write(
                "Intersection x:",
                f"{x_intersection:.4f}",
            )

            st.write(
                "Intersection y:",
                f"{y_intersection:.4f}",
            )

        # Additional information
        st.subheader("Simulation Summary")

        st.write(
            f"Relative volatility: **{alpha:.2f}**"
        )

        st.write(
            f"Distillate composition: **{xD:.2f}**"
        )

        st.write(
            f"Bottoms composition: **{xB:.2f}**"
        )

        st.write(
            f"Feed composition: **{zF:.2f}**"
        )

        st.write(
            f"Operating reflux ratio: **{reflux_ratio:.2f}**"
        )

        st.write(
            f"Feed condition (q): **{q:.2f}**"
        )

        if results["partial_stage"]:

            st.info(
                "The final stage is a partial theoretical stage."
            )

    except ValueError as error:

        st.error(
            f"Simulation error: {error}"
        )

    except RuntimeError as error:

        st.error(
            f"Simulation error: {error}"
        )