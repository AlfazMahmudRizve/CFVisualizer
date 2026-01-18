# Aimbot Trajectory Predictor

## Overview
This visualizer simulates an "aimbot" for a projectile weapon. It accepts a few observed data points (e.g., sensor readings of a grenade's flight) and uses **Numerical Methods** to predict the future trajectory and impact point.

## The Mathematics: Method of Least Squares
The core algorithm is **Polynomial Regression** (specifically, fitting a 2nd-degree parabola: $y = ax^2 + bx + c$).

Since real-world data is noisy or imperfect, we cannot simply solve a system of linear equations for 3 points. Instead, we use the **Method of Least Squares**.

1.  **Goal**: Find coefficients $a, b, c$ that minimize the error between the curve and the data.
2.  **Error Function**: We minimize the "Sum of Squared Residuals":
    $$S = \sum_{i=1}^{n} (y_i - (ax_i^2 + bx_i + c))^2$$
3.  **Solution**: By taking partial derivatives with respect to $a, b, c$ and setting them to zero, we generate a system of normal equations. Solving this matrix yields the "best fit" parabola.

In Python, this is handled via:
```python
coeffs = np.polyfit(len_observed_x, len_observed_y, 2)
```

## Installation
1.  Ensure you have Python installed.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1.  Run the application:
    ```bash
    python cfvisualizer.py
    ```
2.  **Left Click** on the graph to add observed data points.
3.  **Reset**: Clears all points.
4.  **Math**: Shows a popup explanation.

The green line represents the predicted path based on the available data. The cyan point marks the predicted ground impact ($y=0$).
