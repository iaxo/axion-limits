from dash import Dash, html, dcc, Input, Output, State
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
def create_plot(experiments, xrange=(1e-9, 10), yrange=(1e-17, 1e-6), plot_type="AxionGag"):
    #exps = database.get_rows("name", experiments)
    #exps = df[df["name"].isin(experiments)].values.tolist()
    exps = experiments

    print(plot_type)
    if plot_type == "AxionGag":
        plot = AxionGagPlot(
            experiments=exps,
            plotCag=False,
            showplot=False,
            figx=6.5,
            figy=6,
            ymin=yrange[0],
            ymax=yrange[1],
            xmin=xrange[0],
            xmax=xrange[1],
            ticksopt_x="normal",
            ticksopt_y="normal",
        )
        print("AxionGag entrado")
    elif plot_type == "AxionCag":
        plot = AxionGagPlot(
            experiments=exps,
            plotCag=True,
            showplot=False,
            figx=6.5,
            figy=6,
            ymin=yrange[0],
            ymax=yrange[1],
            xmin=xrange[0],
            xmax=xrange[1],
            ticksopt_x="normal",
            ticksopt_y="normal",
            labely=r"$|C_{a\gamma}|\tilde{\rho}_a^{1/2}$",
        )
    elif plot_type == "WIMPSSI":
        plot = WimpPlot(
            experiments=exps,
            showplot=False,
            ymin=yrange[0],
            ymax=yrange[1],
            xmin=xrange[0],
            xmax=xrange[1],
            ticksopt_x="normal",
            ticksopt_y="normal",
        )
    else:
        plot = None
        return ""

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
    
    experiments_init = "exps = " + plot.get_plotted_data_dict_str() + "\n"

    plot_init = f"plot = {plot.__class__.__name__}(\n"
    plot_init += f"    experiments=exps,\n"
    if isinstance(plot, AxionGagPlot):
        plot_init += f"    plotCag={plot.plotCag},\n"
    plot_init += f"    showplot=True,\n"
    plot_init += f"    **{plot.get_plot_customization()}\n"
    plot_init += f")\n"

    return imports + experiments_init + plot_init

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
                                html.Img(
                                    id="curve-plot",
                                    style={"width": "80%", "objectFit": "contain"},
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
