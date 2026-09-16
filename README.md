# McCabe-Thiele Distillation Simulator

A Python-based interactive simulator for the McCabe-Thiele method for binary distillation.

## Overview

This simulator calculates and visualizes theoretical stages required for a binary distillation column using the McCabe-Thiele graphical method. Read more about the method [Here](https://neutrium.net/articles/unit-operations/distillation/mccabe-thiele-plot/)

The simulator uses a constant relative volatility model to calculate the vapor-liquid equilibrium relationship and constructs the rectifying operating line, feed q-line, and stripping operating line.

The simulator allows users to be able to change the main operating and design parameters and be able to visualize the resulting McCabe-Thiele diagram.

## Purpose

This project was developed by Rofhiwa Percy Netshilongwe, a Chemical Engineering student at Vaal University of Technology. The purpose was to learn new technologies like Python, NumPy, Matplotlib, Streamlit and git. The insipiration for this project came from the question "What can i build using things i learned from the classroom that makes life a bit easier?"

## Features

* Binary vapor-liquid equilibrium calculation
* Constant relative volatility model
* Rectifying operating line
* Stripping operating line
* Feed q-line
* Minimum reflux ratio calculation
* Operating-line intersection calculation
* McCabe-Thiele stage stepping
* Theoretical stage count
* Feed-stage identification
* Interactive Streamlit interface
* Input validation and error handling

## Engineering Model

The equilibrium relationship is calculated using:

$$
y^* = \frac{\alpha x}{1 + (\alpha - 1)x}
$$

where:

* \(x\) = liquid-phase mole fraction
* \(y^*\) = equilibrium vapor-phase mole fraction
* \(\alpha\) = relative volatility

The rectifying operating line is:

$$
y = \frac{R}{R+1}x + \frac{x_D}{R+1}
$$

where:

* \(R\) = reflux ratio
* \(x_D\) = distillate composition

For feeds where \(q \neq 1\), the q-line is:

$$
y = \frac{q}{q-1}x - \frac{z_F}{q-1}
$$

For a saturated-liquid feed (\(q=1\)), the q-line is vertical at:

$$
x = z_F
$$

The stripping operating line is constructed using the bottoms composition and the intersection between the rectifying operating line and q-line.

## Running Locally

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in a web browser.

## Running the Tests

The simulation engine can be tested with:

```bash
python test_simulation.py
```

The test checks that a normal simulation runs successfully, that the equilibrium curve has the expected endpoints, and that an invalid reflux ratio is rejected.

## Typical Inputs

The simulator requires:

| Parameter                   | Description                                              |
| --------------------------- | -------------------------------------------------------- |
| Relative volatility (α)     | Relative volatility of the more volatile component       |
| Distillate composition (xD) | Desired mole fraction in the distillate                  |
| Bottoms composition (xB)    | Desired mole fraction in the bottoms                     |
| Feed composition (zF)       | Mole fraction of the more volatile component in the feed |
| Reflux ratio (R)            | Operating reflux ratio                                   |
| Feed condition (q)          | Thermal condition of the feed                            |

## Limitations

The current model assumes:

* Binary mixture
* Constant relative volatility
* Equilibrium stages
* Constant molar overflow
* Steady-state operation
* Idealized McCabe-Thiele assumptions

The simulator is intended for educational and engineering-project purposes not detailed industrial column design.

## Technology

* Python
* NumPy
* Matplotlib
* Streamlit
* Pytest

## Author

Made by Rofhiwa Percy Netshilongwe
View my other [Projects](https://rofhiwapercy.github.io/projects)

## References

1. Lamm, M. H., & Jarboe, L. (2022). *Chemical Engineering Separations: A Handbook for Students — Distillation*. Iowa State University Digital Press / Engineering LibreTexts.
   [Engineering LibreTexts — Distillation](https://eng.libretexts.org/Bookshelves/Chemical_Engineering/Chemical_Engineering_Separations%3A_A_Handbook_for_Students_%28Lamm_and_Jarboe%29/01%3A_Chapters/1.05%3A_Distillation?utm_source=chatgpt.com)

2. Woolf, B. (2020). *ODE and Excel Model of a Simple Distillation Column*. Engineering LibreTexts.
   [Engineering LibreTexts — Distillation Column Model](https://eng.libretexts.org/Bookshelves/Industrial_and_Systems_Engineering/Chemical_Process_Dynamics_and_Controls_%28Woolf%29/06%3A_Modeling_Case_Studies/6.05%3A_ODE_and_Excel_model_of_a_Simple_Distillation_Column?utm_source=chatgpt.com)

3. Coleman, S. (2019). *Distillation Science — Putting It All Together*. Engineering LibreTexts.
   [Engineering LibreTexts — Putting It All Together](https://eng.libretexts.org/Bookshelves/Chemical_Engineering/Distillation_Science_%28Coleman%29/09%3A_Putting_It_All_Together?utm_source=chatgpt.com)