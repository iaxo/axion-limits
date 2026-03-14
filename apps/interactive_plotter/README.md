# Interactive Plotter 🌌📱

A Dash web app for interactively building and exporting publication-quality physics limit plots (axion and WIMP parameter space) powered by the `axionlimits` library.

## Requirements ⚙️

- Python 3.9+
- `axionlimits` python package (see [axionlimits installation guide](../../README.md) for more details).
- `dash`, `dash-ag-grid`:
    ```bash
    cd apps/interactive_plotter
    pip install -r requirements.txt
    ```

## Running the app 👨‍💻

```bash
cd apps/interactive_plotter
python app.py
```

Then open your browser at [http://127.0.0.1:8050](http://127.0.0.1:8050).

### From remote server 🌐🖥️

You can run the app from a remote server too by SSH Port Forwarding. For that, run on your local machine
```bash
ssh -L 8050:localhost:8050 -N -f -l username remote-server-ip
```

---

## Interface overview 🔍

### Plot type selector

Use the dropdown at the top-left to choose what kind of limit plot to display:

| Option | Description |
|---|---|
| **Axions Gag coupling** | Axion–photon coupling $g_{a\gamma}$ vs. mass |
| **Axions Cag coupling** | Axion–photon coupling $C_{a\gamma}$ variant |
| **WIMPS SI coupling** | WIMP spin-independent cross-section vs. mass |

Switching plot type also resets the axis sliders to sensible defaults for that plot.

### Experiment table (right panel)

The AG Grid table lists all available experiments from the database for the selected plot type.

- **Select rows** by clicking the checkbox on the left of each row — selected experiments are drawn on the plot.
- The **`drawOptions`** column is editable: click a cell to modify the drawing style for that experiment (e.g. colour, fill, line style). Changes are reflected in the plot on the next update.

### Axis range sliders

Two `RangeSlider` controls below the plot set the axis limits on a **log₁₀ scale**:

- **X-Axis Range** — sets $\log_{10}(m_a)$ (axion mass in eV) or $\log_{10}(m_\chi)$ (WIMP mass in GeV).
- **Y-Axis Range** — sets $\log_{10}$ of the coupling or cross-section.

You can also type values directly into the numeric inputs on either side of each slider.

---

## Draggable labels 🔤

Labels can be placed freely on top of the plot image.

### Adding labels

Click **Add Label** to create a new text label. It appears in the top-left corner of the plot. You can add as many as you like.

### Editing a label

**Double-click** a label to make it editable. Type the desired text, then click outside or press **Enter** to confirm.

### Moving a label

**Click and drag** a label to reposition it anywhere over the plot.

### Resizing (font size)

Hover over a label and scroll the **mouse wheel** (without holding any modifier key) to increase or decrease the font size (range: 6–72 px).

### Rotating a label

Hover over a label and scroll the **mouse wheel while holding Shift** to rotate it in 2° steps.

### Changing label color

Use the color swatches below the plot to set the color of the **currently selected** label, or click **More colors** to open a full color picker and enter any hex/RGB value.

### Applying labels to the exported plot

The labels shown in the browser are overlaid on the plot image. To bake them into the actual matplotlib figure (so they appear in exports), click **Apply Labels**. The plot will regenerate with all labels placed at their current browser positions, sizes, rotations, and colors.

---

## Exporting 📤

### Python script — Generate 🐍

Downloads a self-contained Python script (`script_generado.py`) that reproduces the current plot using `axionlimits`. You can run it standalone or customise it further.
> [!NOTE]
> Click **Apply Labels** before exporting if you want the labels included in python script.

### PDF — Generate PDF

Downloads a vector PDF (`grafico_generado.pdf`) of the current matplotlib figure, including any applied labels.

> [!NOTE]
> Click **Apply Labels** before exporting if you want the labels included in the PDF.

---

## File structure

```
apps/interactive_plotter/
├── app.py                  # Main Dash application
├── README.md               # This file
└── assets/
    ├── draggable_labels.js # Client-side label drag / edit / wheel logic
    └── styles.css          # Dark-theme CSS overrides
```
