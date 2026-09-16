#APP
#Imports
import streamlit as st
import matplotlib.pyplot as plt
from simulator.simulation import run_simulation

# Page configuration
st.set_page_config(page_title="McCabe-Thiele Simulator", page_icon="None", layout="wide",)
st.title("McCabe-Thiele Distillation Simulator")
st.write(
    "Calculate and visualize theoretical stages for a binary "
    "distillation column using the McCabe-Thiele method."
)

# Input section
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

# Run simulation
run_button = st.sidebar.button(
    "Run Simulation",
    type="primary",
)

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

        # Results
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

            feed_stage = results["feed_stage"]

            if feed_stage is None:
                feed_stage_text = "N/A"
            else:
                feed_stage_text = str(feed_stage)

            st.metric(
                "Feed Stage",
                feed_stage_text,
            )

        # McCabe-Thiele diagram
        st.subheader("McCabe-Thiele Diagram")

        fig, ax = plt.subplots(
            figsize=(8, 8)
        )

        # Equilibrium curve
        ax.plot(
            results["equilibrium_curve"]["x"],
            results["equilibrium_curve"]["y"],
            label="Equilibrium Curve",
        )

        # Diagonal
        ax.plot(
            [0, 1],
            [0, 1],
            linestyle="--",
            label="y = x",
        )

        # Rectifying line
        ax.plot(
            results["rectifying_line"]["x"],
            results["rectifying_line"]["y"],
            label="Rectifying Line",
        )

        # q-line
        ax.plot(
            results["q_line"]["x"],
            results["q_line"]["y"],
            label="q-line",
        )

        # Stripping line
        ax.plot(
            results["stripping_line"]["x"],
            results["stripping_line"]["y"],
            label="Stripping Line",
        )

        # Stage staircase
        stage_x = [
            point[0]
            for point in results["stages"]
        ]

        stage_y = [
            point[1]
            for point in results["stages"]
        ]

        ax.plot(
            stage_x,
            stage_y,
            label="Stages",
            linewidth=1.5,
        )

        # Formatting
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

        ax.grid(True)
        ax.legend()

        st.pyplot(fig)

        # Operating-line information
        st.subheader("Operating Line Information")
        op_col1, op_col2 = st.columns(2)

        with op_col1:
            st.write(
                "Rectifying line slope:",
                f"{results['operating_lines']['rectifying_slope']:.4f}",
            )
            st.write(
                "Rectifying line intercept:",
                f"{results['operating_lines']['rectifying_intercept']:.4f}",
            )
        with op_col2:
            st.write(
                "Operating-line intersection x:",
                f"{results['operating_lines']['x_intersection']:.4f}",
            )
            st.write(
                "Operating-line intersection y:",
                f"{results['operating_lines']['y_intersection']:.4f}",
            )
-
        # Simulation inputs
        with st.expander("Simulation Inputs"):

            st.write(
                f"Relative volatility α: {alpha}"
            )

            st.write(
                f"Distillate composition xD: {xD}"
            )

            st.write(
                f"Bottoms composition xB: {xB}"
            )

            st.write(
                f"Feed composition zF: {zF}"
            )

            st.write(
                f"Reflux ratio R: {reflux_ratio}"
            )

            st.write(
                f"Feed condition q: {q}"
            )

    except ValueError as error:

        st.error(
            f"Simulation error: {error}"
        )

    except RuntimeError as error:

        st.error(
            f"Simulation error: {error}"
        )