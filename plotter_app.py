from dash import Dash, html, dcc, Input, Output, State, ClientsideFunction
import dash_ag_grid as dag
import axionlimits.databases as db
from axionlimits.axion_plot import AxionGagPlot
from axionlimits.wimp_plot import WimpPlot
from axionlimits.utils import resolve_relative_path
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import pandas as pd
import io
import base64

mpl.use("Agg")

GENERATED_PLOT = None
def _parse_css_px(value, default=0.0):
    """Parse CSS pixel values like '24px' to float."""
    if value is None:
        return float(default)
    if isinstance(value, (int, float)):
        return float(value)
    txt = str(value).strip().lower().replace("px", "")
    try:
        return float(txt)
    except ValueError:
        return float(default)


def get_mpl_labels_from_drawn_labels(
    labels_layer_children,
    layer_width,
    layer_height,
    x_anchor="left",
    y_anchor="top",
):
    """Convert drawn Dash labels into mpl-ready text coordinates.

    Returns a list of dicts with keys: text, xpos_mpl, ypos_mpl.
    """
    labels_mpl = []
    for label in labels_layer_children or []:
        props = label.get("props", {}) if isinstance(label, dict) else {}
        style = props.get("style", {}) if isinstance(props, dict) else {}

        text = props.get("children", "")
        if isinstance(text, list):
            text = " ".join(str(item) for item in text)
        text = str(text).strip()
        if not text:
            continue

        label_data = {
            "left": _parse_css_px(style.get("left", 0)),
            "top": _parse_css_px(style.get("top", 0)),
            "width": _parse_css_px(style.get("width", 0)),
            "height": _parse_css_px(style.get("height", 0)),
            "layerWidth": float(layer_width),
            "layerHeight": float(layer_height),
        }
        coords = label_browser_to_mpl_figure_coords(
            label_data, x_anchor=x_anchor, y_anchor=y_anchor
        )
        if not coords:
            continue

        xpos_mpl, ypos_mpl = coords
        labels_mpl.append(
            {
                "text": text,
                "xpos_mpl": xpos_mpl,
                "ypos_mpl": ypos_mpl,
            }
        )

    return labels_mpl


def create_plot_from_drawn_labels(
    experiments,
    labels_layer_children,
    layer_width,
    layer_height,
    xrange=(1e-9, 10),
    yrange=(1e-17, 1e-6),
    plot_type="AxionGag",
    x_anchor="left",
    y_anchor="top",
):
    """Convert drawn labels and render them in create_plot for quick testing."""
    labels_mpl = get_mpl_labels_from_drawn_labels(
        labels_layer_children,
        layer_width,
        layer_height,
        x_anchor=x_anchor,
        y_anchor=y_anchor,
    )
    return create_plot(
        experiments=experiments,
        xrange=xrange,
        yrange=yrange,
        plot_type=plot_type,
        labels_mpl=labels_mpl,
    )


def create_plot(
    experiments,
    xrange=(1e-9, 10),
    yrange=(1e-17, 1e-6),
    plot_type="AxionGag",
    labels_mpl=None,
):
    #exps = database.get_rows("name", experiments)
    #exps = df[df["name"].isin(experiments)].values.tolist()
    exps = experiments

    def _convert_labels_for_plot_constructor(plot_obj, labels_for_plot):
        """Convert figure-fraction label positions to data coordinates for plot.labels."""
        converted = []
        fig_w_px, fig_h_px = plot_obj.fig.get_size_inches() * plot_obj.fig.dpi
        axes_bbox = plot_obj.plot.get_position()
        x0_ax, y0_ax, x1_ax, y1_ax = (
            axes_bbox.x0,
            axes_bbox.y0,
            axes_bbox.x1,
            axes_bbox.y1,
        )
        ax_w = max(x1_ax - x0_ax, 1e-12)
        ax_h = max(y1_ax - y0_ax, 1e-12)

        for label in labels_for_plot or []:
            text = str(label.get("text", "")).strip()
            if not text:
                continue

            x_fig = float(label.get("xpos_mpl", 0.0))
            y_fig = float(label.get("ypos_mpl", 0.0))
            x_fig = min(max(x_fig, 0.0), 1.0)
            y_fig = min(max(y_fig, 0.0), 1.0)

            # Convert figure fractions to axes fractions and clamp to visible axes region.
            x_ax = min(max((x_fig - x0_ax) / ax_w, 0.0), 1.0)
            y_ax = min(max((y_fig - y0_ax) / ax_h, 0.0), 1.0)

            # Map axes coordinates to data coordinates using matplotlib transforms.
            x_disp, y_disp = plot_obj.plot.transAxes.transform((x_ax, y_ax))
            x_data, y_data = plot_obj.plot.transData.inverted().transform((x_disp, y_disp))

            # Match browser font size: CSS px -> figure px -> matplotlib points.
            font_px_browser = float(label.get("font_size_px", 13.0) or 13.0)
            layer_w = float(label.get("layer_width_px", 0.0) or 0.0)
            layer_h = float(label.get("layer_height_px", 0.0) or 0.0)
            scale_x = fig_w_px / layer_w if layer_w > 0 else 1.0
            scale_y = fig_h_px / layer_h if layer_h > 0 else 1.0
            fig_px_font = font_px_browser * min(scale_x, scale_y)
            font_size_pt = max(fig_px_font * 72.0 / plot_obj.fig.dpi, 1.0)
            rotation_deg = float(label.get("rotation_deg", 0.0) or 0.0)

            text_style = {
                "color": "black",
                "size": font_size_pt,
                "ha": "left",
                "va": "top",
                "rotation": -rotation_deg,
                "rotation_mode": "anchor",
                "picker": True,
            }
            converted.append((text, float(x_data), float(y_data), text_style))
        return converted

    print(plot_type)
    if plot_type == "AxionGag":
        plot_class = AxionGagPlot
        plot_kwargs = {
            "experiments": exps,
            "plotCag": False,
            "showplot": False,
            "figx": 6.5,
            "figy": 6,
            "ymin": yrange[0],
            "ymax": yrange[1],
            "xmin": xrange[0],
            "xmax": xrange[1],
            "ticksopt_x": "normal",
            "ticksopt_y": "normal",
        }
        print("AxionGag entrado")
    elif plot_type == "AxionCag":
        plot_class = AxionGagPlot
        plot_kwargs = {
            "experiments": exps,
            "plotCag": True,
            "showplot": False,
            "figx": 6.5,
            "figy": 6,
            "ymin": yrange[0],
            "ymax": yrange[1],
            "xmin": xrange[0],
            "xmax": xrange[1],
            "ticksopt_x": "normal",
            "ticksopt_y": "normal",
            "labely": r"$|C_{a\gamma}|\tilde{\rho}_a^{1/2}$",
        }
    elif plot_type == "WIMPSSI":
        plot_class = WimpPlot
        plot_kwargs = {
            "experiments": exps,
            "showplot": False,
            "ymin": yrange[0],
            "ymax": yrange[1],
            "xmin": xrange[0],
            "xmax": xrange[1],
            "ticksopt_x": "normal",
            "ticksopt_y": "normal",
        }
    else:
        return ""

    # First build without labels to compute exact data coordinates via transforms.
    plot = plot_class(labels=[], **plot_kwargs)

    if labels_mpl:
        labels_for_constructor = _convert_labels_for_plot_constructor(plot, labels_mpl)
        plt.close(plot.fig)
        plot = plot_class(labels=labels_for_constructor, **plot_kwargs)

    global GENERATED_PLOT
    GENERATED_PLOT = plot

    buffer = io.BytesIO()
    plot.fig.savefig(buffer, format="png")
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.read()).decode()
    plt.close(plot.fig)
    return f"data:image/png;base64,{encoded_image}"

def generate_plotting_script_str(plot, filename="plotting_script.py"):
    imports = "import axionlimits.databases as db\n"
    if isinstance(plot, AxionGagPlot):
        imports += "from axionlimits.axion_plot import AxionGagPlot\n"
    elif isinstance(plot, WimpPlot):
        imports += "from axionlimits.wimp_plot import WimpPlot\n"
    imports += "import numpy as np\n\n"
    
    experiments_init = "exps = " + plot.get_plotted_data_dict_str() + "\n"
    labels_init = "labels = " + plot.get_plot_labels_str() + "\n"

    plot_init = f"plot = {plot.__class__.__name__}(\n"
    plot_init += f"    experiments=exps,\n"
    plot_init += f"    labels=labels,\n"
    if isinstance(plot, AxionGagPlot):
        plot_init += f"    plotCag={plot.plotCag},\n"
    plot_init += f"    showplot=True,\n"
    plot_init += f"    **{plot.get_plot_customization()}\n"
    plot_init += f")\n"

    return imports + experiments_init + labels_init + plot_init


def label_browser_to_mpl_figure_coords(
    label,
    x_anchor="left",
    y_anchor="top",
):
    """Convert a browser label position (pixels) into matplotlib figure coordinates.

    Expected label keys:
    - left, top: label position in pixels inside the overlay layer.
    - layerWidth, layerHeight: overlay layer size in pixels.
    - width, height (optional): label box size in pixels, used for anchor offsets.

    Returns:
    - (x_fig, y_fig) in figure fraction coordinates [0, 1], or None if input is invalid.
    """
    layer_width = float(label.get("layerWidth", 0) or 0)
    layer_height = float(label.get("layerHeight", 0) or 0)
    if layer_width <= 0 or layer_height <= 0:
        return None

    left_px = float(label.get("left", 0) or 0)
    top_px = float(label.get("top", 0) or 0)
    label_width = float(label.get("width", 0) or 0)
    label_height = float(label.get("height", 0) or 0)

    x_px = left_px
    y_px = top_px

    if x_anchor == "center":
        x_px += 0.5 * label_width
    elif x_anchor == "right":
        x_px += label_width

    if y_anchor == "center":
        y_px += 0.5 * label_height
    elif y_anchor == "bottom":
        y_px += label_height

    x_fig = x_px / layer_width
    y_fig = 1.0 - (y_px / layer_height)

    x_fig = min(max(x_fig, 0.0), 1.0)
    y_fig = min(max(y_fig, 0.0), 1.0)
    return x_fig, y_fig


def get_mpl_labels_from_browser_snapshot(labels_snapshot):
    """Convert synced browser labels into {text, xpos_mpl, ypos_mpl} list."""
    labels_mpl = []
    for label in labels_snapshot or []:
        coords = label_browser_to_mpl_figure_coords(label)
        if not coords:
            continue
        text = str(label.get("text", "")).strip()
        if not text:
            continue
        xpos_mpl, ypos_mpl = coords
        labels_mpl.append(
            {
                "text": text,
                "xpos_mpl": xpos_mpl,
                "ypos_mpl": ypos_mpl,
                "font_size_px": float(label.get("fontSizePx", 13.0) or 13.0),
                "rotation_deg": float(label.get("rotationDeg", 0.0) or 0.0),
                "layer_width_px": float(label.get("layerWidth", 0.0) or 0.0),
                "layer_height_px": float(label.get("layerHeight", 0.0) or 0.0),
            }
        )
    return labels_mpl

# Initialize Dash app
app = Dash(__name__)
app.title = "Interactive Axion Limits"

# Load database
database = db.DataBaseGag()
df = database.get_pandas_dataframe()

# Dropdown options for databases
databases_path = resolve_relative_path("")
dropdown_options = []
for f in os.listdir(databases_path):
    if f.endswith(".db"):
        db_ = db.DataBase(f"{databases_path}/{f}", "")
        dropdown_options.extend([
            {"label": f"{f}, {table}", "value": f"{databases_path}/{f};{table}"}
            for table in db_.get_table_names()
        ])

# Dropdown options for plot types
plot_options = [
    {"label": "Axions Gag coupling", "value": "AxionGag"},
    {"label": "Axions Cag coupling", "value": "AxionCag"},
    {"label": "Axions Gae coupling", "value": "AxionGae"},
    {"label": "WIMPS SI coupling", "value": "WIMPSSI"},
]
plot_option_database = {
    "AxionGag": db.DataBaseGag,
    "AxionCag": db.DataBaseGag,
    "AxionGae": db.DataBaseGae,
    "WIMPSSI": db.DataBaseWimps,
}


# Define column definitions for AgGrid
columns_defs = [
    {
        "headerCheckboxSelection": True,
        "checkboxSelection": True,
        "field": "checkbox",
        "headerName": "",
        "width": 80,
    }
]
columns_defs.extend([{"field": col, "headerName": col} for col in df.columns])
# make drawOptions editable
for col in columns_defs:
    if col["field"] == "checkbox":
        col["pinned"] = "left"
    if col["field"] == "name":
        col["pinned"] = "left"
    if col["field"] == "drawOptions":
        col["editable"] = True


# Layout
app.layout = html.Div(
    children=[
        dcc.Store(id="labels-dom-store", data=[]),
        dcc.Interval(id="labels-sync-interval", interval=300, n_intervals=0),
        html.H1(
            "Interactive Dark Matter Limits Graphs",
            style={
                "textAlign": "center",
                "color": "#ffffff",
                "marginBottom": "20px",
                "textShadow": "2px 2px 5px rgba(0, 0, 0, 0.7)",
                "fontSize": "54px",
            },
        ),
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "flex-start",
                "gap": "20px",
            },
            children=[
                # Left Section (Plot type selector and sliders)
                html.Div(
                    style={"width": "50%"},
                    children=[
                        dcc.Dropdown(                    
                            id="plot-type-selector",
                            options=plot_options,
                            #value=plot_options[0]['value'],  # Set a default value
                            placeholder="Select a Plot Type",
                            style={"width": "100%", "marginBottom": "10px"},
                            className="dark-theme",
                        ),
                        html.Div(
                            id="plot-container",
                            style={
                                "backgroundColor": "#2e2e3d",
                                "padding": "20px",
                                "borderRadius": "10px",
                                "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.5)",
                                "flex": "1",  # Flexible height allocation
                                "display": "flex",
                                "justifyContent": "center",
                                "alignItems": "center",
                            },
                            children=[
                                html.Div(
                                    id="plot-overlay-wrapper",
                                    style={
                                        "position": "relative",
                                        "width": "80%",
                                        "display": "inline-block",
                                    },
                                    children=[
                                        html.Img(
                                            id="curve-plot",
                                            style={"width": "100%", "objectFit": "contain"},
                                        ),
                                        html.Div(id="labels-layer", className="labels-layer"),
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            style={
                                "marginTop": "10px",
                                "display": "flex",
                                "gap": "10px",
                            },
                            children=[
                                html.Button(
                                    "Add Label",
                                    id="btn-add-label",
                                    n_clicks=0,
                                    style={
                                        "backgroundColor": "#1f7a8c",
                                        "color": "white",
                                        "padding": "8px 18px",
                                        "border": "none",
                                        "cursor": "pointer",
                                        "borderRadius": "5px",
                                        "fontSize": "16px",
                                    },
                                ),
                                html.Button(
                                    "Apply Labels",
                                    id="btn-apply-labels",
                                    n_clicks=0,
                                    style={
                                        "backgroundColor": "#2d6a4f",
                                        "color": "white",
                                        "padding": "8px 18px",
                                        "border": "none",
                                        "cursor": "pointer",
                                        "borderRadius": "5px",
                                        "fontSize": "16px",
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            children=[
                                dcc.RangeSlider(
                                    id="x-range-slider",
                                    min=-15, max=15, step=0.1,
                                    marks={i: str(i) for i in range(-15, 16, 2)},
                                    value=[-11, 9],
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    className="dark-theme",
                                ),
                                html.Div(
                                    "X-Axis Range",
                                    style={"textAlign": "center", "marginTop": "10px"},
                                ),
                            ],
                            style={"marginBottom": "20px", "marginTop": "20px"},
                        ),
                        html.Div(
                            children=[
                                dcc.RangeSlider(
                                    id="y-range-slider",
                                    min=-20, max=5, step=0.1,
                                    marks={i: str(i) for i in range(-20, 6, 2)},
                                    value=[-18, -4],
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    className="dark-theme",
                                ),
                                html.Div(
                                    "Y-Axis Range",
                                    style={"textAlign": "center", "marginTop": "10px"},
                                ),
                            ],
                        ),
                    ],
                ),
                # Right Section (Database selector and AgGrid)
                html.Div(
                    style={"width": "50%"},
                    children=[
                        dag.AgGrid(
                            id="ag-grid",
                            columnDefs=columns_defs,
                            rowData=df.to_dict("records"),
                            style={"height": "80vh", "width": "100%"},
                            dashGridOptions={"rowSelection": "multiple"},
                            className="ag-theme-alpine-dark",
                        ),
                        # Container for the two buttons side by side
                        html.Div(
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "flex-start",
                                "marginTop": "10px",
                            },
                            children=[
                                # Container for the Generate 🐍 button
                                html.Div(
                                    children=[
                                        html.Button(
                                            "Generate 🐍",
                                            id="btn-generate-py",
                                            n_clicks=0,
                                            style={
                                                "backgroundColor": "#4CAF50",
                                                "color": "white",
                                                "padding": "10px 24px",
                                                "border": "none",
                                                "cursor": "pointer",
                                                "borderRadius": "5px",
                                                "fontSize": "24px",
                                            },
                                        ),
                                        dcc.Download(id="download-py"),
                                    ],
                                    style={"marginRight": "20px"},  # separation between buttons
                                ),
                                # Container for the Generate PDF button
                                html.Div(
                                    children=[
                                        html.Button(
                                            "Generate PDF",
                                            id="btn-generate-pdf",
                                            n_clicks=0,
                                            style={
                                                "backgroundColor": "#8b2b2b",
                                                "color": "white",
                                                "padding": "10px 24px",
                                                "border": "none",
                                                "cursor": "pointer",
                                                "borderRadius": "5px",
                                                "fontSize": "24px",
                                            },
                                        ),
                                        dcc.Download(id="download-pdf"),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)

app.clientside_callback(
    ClientsideFunction(namespace="labels", function_name="snapshot"),
    Output("labels-dom-store", "data"),
    Input("labels-sync-interval", "n_intervals"),
)

# Callbacks
@app.callback(
    Output("curve-plot", "src"),
    Input("x-range-slider", "value"),
    Input("y-range-slider", "value"),
    Input("ag-grid", "selectedRows"),
    Input("ag-grid", "cellValueChanged"),
    Input("plot-type-selector", "value"),
)
def update_plot_axis_ranges(x_range, y_range, selected_curves, cell_changed, plot_type):
    if not selected_curves:
        selected_curves = []
    print("selected curves en el callback", selected_curves)
    exps={}
    for row in selected_curves:
        exps[row["name"]] = row.copy()
    return create_plot(
        experiments=exps,
        xrange=(10 ** x_range[0], 10 ** x_range[1]),
        yrange=(10 ** y_range[0], 10 ** y_range[1]),
        plot_type=plot_type,
    )

# change sliders range
@app.callback(
    Output("x-range-slider", "min"),
    Output("x-range-slider", "max"),
    Output("x-range-slider", "value"),
    Output("y-range-slider", "min"),
    Output("y-range-slider", "max"),
    Output("y-range-slider", "value"),
    Input("plot-type-selector", "value"),
)
def update_sliders_ranges(plot_type):
    if plot_type == "AxionGag":
        return -15, 15, (-11, 9), -20, 5, (-18, -4)
    elif plot_type == "AxionCag":
        return -20, 10, (-9, 0), -10, 10, (-1, 3)
    elif plot_type == "AxionGae":
        return -15, 15, (-11, 9), -20, 5, (-18, -4)
    elif plot_type == "WIMPSSI":
        return -5, 5, (-1, 1), -60, -25, (-46, -34)
    return -15, 15, (-11, 9), -20, 5, (-18, -4)

@app.callback(
    Output("ag-grid", "rowData"),
    Input("plot-type-selector", "value"),
)
def select_database(plot_type):
    if not plot_type:
        return []
    db_selected = plot_option_database.get(plot_type, None)
    df = db_selected().get_pandas_dataframe()
    return df.to_dict("records")

# Update data on cell value change
@app.callback(
    Output("ag-grid", "rowData", allow_duplicate=True),
    Input("ag-grid", "cellValueChanged"),
    State("ag-grid", "rowData"),
    prevent_initial_call=True,
)
def update_drawOptions(cell_changed, data):
    if not cell_changed:
        return data
    df = pd.DataFrame(data)
    return df.to_dict("records")


@app.callback(
    Output("labels-layer", "children"),
    Input("btn-add-label", "n_clicks"),
    State("labels-layer", "children"),
    prevent_initial_call=True,
)
def add_draggable_label(n_clicks, existing_labels):
    labels = existing_labels if existing_labels else []
    labels.append(
        html.Div(
            f"Label {n_clicks}",
            className="draggable-label",
            style={
                "left": f"{20 + (n_clicks - 1) * 12}px",
                "top": f"{20 + (n_clicks - 1) * 12}px",
            },
        )
    )
    return labels


@app.callback(
    Output("curve-plot", "src", allow_duplicate=True),
    Input("btn-apply-labels", "n_clicks"),
    State("x-range-slider", "value"),
    State("y-range-slider", "value"),
    State("ag-grid", "selectedRows"),
    State("plot-type-selector", "value"),
    State("labels-dom-store", "data"),
    prevent_initial_call=True,
)
def apply_labels_to_current_plot(
    n_clicks,
    x_range,
    y_range,
    selected_curves,
    plot_type,
    labels_snapshot,
):
    if not selected_curves:
        selected_curves = []

    exps = {}
    for row in selected_curves:
        exps[row["name"]] = row.copy()

    labels_mpl = get_mpl_labels_from_browser_snapshot(labels_snapshot)
    return create_plot(
        experiments=exps,
        xrange=(10 ** x_range[0], 10 ** x_range[1]),
        yrange=(10 ** y_range[0], 10 ** y_range[1]),
        plot_type=plot_type,
        labels_mpl=labels_mpl,
    )

@app.callback(
    Output("download-py", "data"),
    Input("btn-generate-py", "n_clicks"),
    prevent_initial_call=True
)
def generate_python_file(n_clicks):
    # Contenido del archivo Python como un string
    python_code = generate_plotting_script_str(GENERATED_PLOT)
    # Enviar el archivo para descarga
    return dict(content=python_code, filename="script_generado.py", type="text/plain")

@app.callback(
    Output("download-pdf", "data"),
    Input("btn-generate-pdf", "n_clicks"),
    prevent_initial_call=True
)
def generate_pdf_file(n_clicks):
    # Guardar la figura en un buffer de memoria
    buffer = io.BytesIO()
    GENERATED_PLOT.fig.savefig(buffer, format="pdf")  # Guardar como PDF
    buffer.seek(0)  # Ir al inicio del buffer
    # Enviar el contenido del buffer como bytes para descarga
    return dcc.send_bytes(buffer.getvalue(), filename="grafico_generado.pdf")


if __name__ == "__main__":
    app.run(debug=True)
