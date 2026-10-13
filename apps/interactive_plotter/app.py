from dash import Dash, html, dcc, Input, Output, State, ClientsideFunction, ctx, no_update
import dash_ag_grid as dag
import axionlimits.databases as db
from axionlimits.axion_plot import AxionGagPlot
from axionlimits.wimp_plot import WimpPlot
from axionlimits.utils import resolve_relative_path
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import os
import pandas as pd
import io
import base64
import re
import math
import inspect
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

mpl.use("Agg")

GENERATED_PLOT = None
# What the last plot was built from (class, constructor kwargs, arrows), used to
# generate the python script.
GENERATED_SPEC = None
LABEL_FONT_SCALE_CORRECTION = 1.12
LABEL_VERTICAL_OFFSET_TUNE = 2.24
LABEL_CSS_LINE_HEIGHT = 1.2  # line-height of .draggable-label in styles.css
DEFAULT_LAYER_WIDTH_PX = 600.0  # fallback when the overlay size is not known yet

ARROW_STYLES = ("-", "->", "-|>", "<-", "<|-", "<->", "<|-|>")

SCRIPT_IMPORTER = Path(__file__).with_name("script_importer.py")
SCRIPT_IMPORT_TIMEOUT_S = 120

# Slider ranges (log10) and figure size used when selecting each plot type.
PLOT_TYPE_DEFAULTS = {
    "AxionGag": {"x": (-15, 15, [-11, 9]), "y": (-20, 5, [-18, -4]), "figsize": (6.5, 6)},
    "AxionCag": {"x": (-20, 10, [-9, 0]), "y": (-10, 10, [-1, 3]), "figsize": (6.5, 6)},
    "AxionGae": {"x": (-15, 15, [-11, 9]), "y": (-20, 5, [-18, -4]), "figsize": (6.5, 6)},
    "WIMPSSI": {"x": (-5, 5, [-1, 1]), "y": (-60, -25, [-46, -34]), "figsize": (9, 7)},
}


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


def _normalize_css_color_for_mpl(value, default="black"):
    """Convert browser CSS color strings to matplotlib-compatible color strings."""
    if value is None:
        return default

    text = str(value).strip()
    if not text:
        return default

    lowered = text.lower()
    if lowered.startswith("#"):
        return text

    if lowered.startswith("rgb(") or lowered.startswith("rgba("):
        matches = re.findall(r"[0-9]*\.?[0-9]+", lowered)
        if len(matches) >= 3:
            try:
                r = int(float(matches[0]))
                g = int(float(matches[1]))
                b = int(float(matches[2]))
                r = min(max(r, 0), 255)
                g = min(max(g, 0), 255)
                b = min(max(b, 0), 255)

                if len(matches) >= 4:
                    a_raw = float(matches[3])
                    # rgba() alpha can be 0..1 in CSS; clamp to matplotlib expected range.
                    a = min(max(a_raw, 0.0), 1.0)
                    a_hex = int(round(a * 255))
                    return f"#{r:02x}{g:02x}{b:02x}{a_hex:02x}"

                return f"#{r:02x}{g:02x}{b:02x}"
            except ValueError:
                return default

    # Named colors (e.g. 'black', 'white') pass through unchanged.
    return text


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
                "color": _normalize_css_color_for_mpl(style.get("color", "black")),
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
    ticksopt_x="normal",
    ticksopt_y="normal",
    figx=None,
    figy=None,
    arrows_mpl=None,
    extra_kwargs=None,
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

            # Match browser font size: CSS px -> figure px -> matplotlib points.
            font_px_browser = float(label.get("font_size_px", 13.0) or 13.0)
            line_height_px_browser = float(
                label.get("line_height_px", font_px_browser * 1.2)
                or (font_px_browser * 1.2)
            )
            layer_w = float(label.get("layer_width_px", 0.0) or 0.0)
            layer_h = float(label.get("layer_height_px", 0.0) or 0.0)
            scale_x = fig_w_px / layer_w if layer_w > 0 else 1.0
            scale_y = fig_h_px / layer_h if layer_h > 0 else 1.0
            fig_px_font = font_px_browser * min(scale_x, scale_y)
            # Browser text sits inside the line-height box with half-leading on top.
            top_leading_px = max(
                (line_height_px_browser - font_px_browser)
                * 0.5
                * LABEL_VERTICAL_OFFSET_TUNE,
                0.0,
            )
            # Rounded so that the app image and the generated script (which prints
            # rounded sizes) render identically, e.g. 9 instead of 8.99998.
            font_size_pt = round(
                max(
                    fig_px_font * 72.0 / plot_obj.fig.dpi * LABEL_FONT_SCALE_CORRECTION,
                    1.0,
                ),
                2,
            )

            rotation_deg = float(label.get("rotation_deg", 0.0) or 0.0)
            theta = math.radians(rotation_deg)
            # Apply top-leading correction in label-local +y direction (rotated in browser).
            offset_x_browser = -math.sin(theta) * top_leading_px
            offset_y_browser = math.cos(theta) * top_leading_px
            x_disp += offset_x_browser * scale_x
            y_disp -= offset_y_browser * scale_y
            x_data, y_data = plot_obj.plot.transData.inverted().transform((x_disp, y_disp))

            text_color = str(label.get("color", "black") or "black")
            text_color = _normalize_css_color_for_mpl(text_color, default="black")

            # Extra matplotlib options (e.g. bc/bw borders from an imported script)
            # never override what the overlay controls.
            extra = label.get("extra") or {}
            text_style = {
                **(extra if isinstance(extra, dict) else {}),
                "color": text_color,
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
    plot_class, plot_kwargs = get_plot_class_and_kwargs(
        plot_type,
        experiments=exps,
        xrange=xrange,
        yrange=yrange,
        ticksopt_x=ticksopt_x,
        ticksopt_y=ticksopt_y,
        figx=figx,
        figy=figy,
        extra_kwargs=extra_kwargs,
    )
    if plot_class is None:
        return ""

    # First build without labels to compute exact data coordinates via transforms.
    plot = plot_class(labels=[], **plot_kwargs)

    labels_for_constructor = []
    if labels_mpl:
        labels_for_constructor = _convert_labels_for_plot_constructor(plot, labels_mpl)
        plt.close(plot.fig)
        # plot_labels() modifies the style dicts (bc/bw -> path_effects): pass
        # copies so that labels_for_constructor can still be written to a script.
        plot = plot_class(
            labels=[(t, x, y, dict(style)) for t, x, y, style in labels_for_constructor],
            **plot_kwargs,
        )

    arrows_for_plot = convert_arrows_for_plot(plot, arrows_mpl)
    draw_arrows(plot, arrows_for_plot)

    global GENERATED_PLOT, GENERATED_SPEC
    GENERATED_PLOT = plot
    GENERATED_SPEC = {
        "class": plot_class,
        "kwargs": {**plot_kwargs, "labels": labels_for_constructor},
        "arrows": arrows_for_plot,
        "labelx": plot.plot.get_xlabel(),
        "labely": plot.plot.get_ylabel(),
    }

    buffer = io.BytesIO()
    plot.fig.savefig(buffer, format="png")
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.read()).decode()
    plt.close(plot.fig)
    return f"data:image/png;base64,{encoded_image}"

def get_plot_class_and_kwargs(
    plot_type,
    experiments=None,
    xrange=(1e-9, 10),
    yrange=(1e-17, 1e-6),
    ticksopt_x="normal",
    ticksopt_y="normal",
    figx=None,
    figy=None,
    extra_kwargs=None,
):
    """Plot class and constructor kwargs (without labels) for a plot type."""
    if plot_type not in ("AxionGag", "AxionCag", "WIMPSSI"):
        return None, None

    default_figx, default_figy = PLOT_TYPE_DEFAULTS[plot_type]["figsize"]
    plot_kwargs = {
        "experiments": experiments if experiments is not None else {},
        "showplot": False,
        "figx": float(figx) if figx else default_figx,
        "figy": float(figy) if figy else default_figy,
        "ymin": yrange[0],
        "ymax": yrange[1],
        "xmin": xrange[0],
        "xmax": xrange[1],
        "ticksopt_x": ticksopt_x,
        "ticksopt_y": ticksopt_y,
    }
    if plot_type == "AxionGag":
        plot_class = AxionGagPlot
        plot_kwargs["plotCag"] = False
    elif plot_type == "AxionCag":
        plot_class = AxionGagPlot
        plot_kwargs["plotCag"] = True
        plot_kwargs["labely"] = r"$|C_{a\gamma}|\tilde{\rho}_a^{1/2}$"
    else:
        plot_class = WimpPlot

    # Constructor options imported from a script that have no control in the app.
    extra = dict(extra_kwargs or {})
    excluded_region_options = extra.pop("excludedRegionOptions", None) or {}
    if plot_class is WimpPlot:
        plot_kwargs.update(excluded_region_options)
    else:
        extra.pop("excludedRegion", None)
    plot_kwargs.update(extra)
    return plot_class, plot_kwargs


def get_app_default_constructor_kwargs(plot_type):
    """Constructor kwargs the app uses for a plot type (class defaults included)."""
    plot_class, plot_kwargs = get_plot_class_and_kwargs(plot_type)
    if plot_class is None:
        return {}
    defaults = {
        name: param.default
        for name, param in inspect.signature(plot_class.__init__).parameters.items()
        if param.default is not inspect.Parameter.empty
    }
    defaults.update(plot_kwargs)
    return defaults


def convert_arrows_for_plot(plot_obj, arrows_mpl):
    """Convert arrows in figure fractions into (x0, y0, x1, y1, kwargs) in data coords."""
    converted = []
    to_data = plot_obj.plot.transData.inverted()
    for arrow in arrows_mpl or []:
        try:
            start = plot_obj.fig.transFigure.transform((float(arrow["x0"]), float(arrow["y0"])))
            end = plot_obj.fig.transFigure.transform((float(arrow["x1"]), float(arrow["y1"])))
        except (KeyError, TypeError, ValueError):
            continue
        x0, y0 = to_data.transform(start)
        x1, y1 = to_data.transform(end)
        style = arrow.get("arrowstyle")
        arrow_kwargs = {
            "arrowstyle": style if style in ARROW_STYLES else "-|>",
            "color": _normalize_css_color_for_mpl(arrow.get("color"), default="black"),
            "linewidth": round(float(arrow.get("lw", 1.0) or 1.0), 3),
            "mutation_scale": round(float(arrow.get("mutation_scale", 12.0) or 12.0), 3),
            "shrinkA": 0,
            "shrinkB": 0,
            # do not clip so that arrows look like in the browser overlay
            "clip_on": False,
        }
        converted.append((float(x0), float(y0), float(x1), float(y1), arrow_kwargs))
    return converted


def draw_arrows(plot_obj, arrows):
    for x0, y0, x1, y1, arrow_kwargs in arrows or []:
        plot_obj.plot.add_patch(FancyArrowPatch((x0, y0), (x1, y1), **arrow_kwargs))


def _format_script_value(value, digits=6):
    if isinstance(value, float):
        return f"{value + 0.0:.{digits}g}"  # + 0.0 turns -0.0 into 0.0
    if isinstance(value, dict):
        return "dict(" + ", ".join(
            f"{k}={_format_script_value(v, 4)}" for k, v in value.items()
        ) + ")"
    return repr(value)


def _format_script_text(text):
    """Raw string literal when possible, as in hand-written scripts."""
    if "'" not in text and "\n" not in text and not text.endswith("\\"):
        return f"r'{text}'"
    return repr(text)


def _experiments_for_script(experiments, plot_class):
    result = {}
    for name, info in (experiments or {}).items():
        draw_options = info.get("drawOptions", "")
        if not isinstance(draw_options, (str, dict)):
            draw_options = ""
        properties = {
            "type": info.get("type", ""),
            "path": info.get("path", ""),
            "drawOptions": draw_options,
        }
        if plot_class is WimpPlot and info.get("projection"):
            properties["projection"] = True
        result[name] = properties
    return result


def generate_plotting_script_str(spec, filename="plotting_script.py"):
    plot_class = spec["class"]
    kwargs = spec["kwargs"]
    arrows = spec.get("arrows") or []

    imports = "import axionlimits.databases as db\n"
    if plot_class is AxionGagPlot:
        imports += "from axionlimits.axion_plot import AxionGagPlot\n"
    elif plot_class is WimpPlot:
        imports += "from axionlimits.wimp_plot import WimpPlot\n"
    if arrows:
        imports += "from matplotlib.patches import FancyArrowPatch\n"
    imports += "import numpy as np\n\n"

    experiments = _experiments_for_script(kwargs.get("experiments"), plot_class)
    experiments_init = "exps = {\n"
    for name, properties in experiments.items():
        experiments_init += f"    {name!r}: {properties!r},\n"
    experiments_init += "}\n"

    labels_init = "labels = [\n"
    for text, x, y, style in kwargs.get("labels") or []:
        style = {k: v for k, v in style.items() if k != "picker"}
        labels_init += (
            f"    ({_format_script_text(text)}, {_format_script_value(x)}, "
            f"{_format_script_value(y)}, {_format_script_value(style)}),\n"
        )
    labels_init += "]\n"

    arrows_init = ""
    if arrows:
        arrows_init = "arrows = [  # (x_start, y_start, x_end, y_end, FancyArrowPatch options)\n"
        for x0, y0, x1, y1, arrow_kwargs in arrows:
            coords = ", ".join(_format_script_value(v) for v in (x0, y0, x1, y1))
            arrows_init += f"    ({coords}, {_format_script_value(arrow_kwargs)}),\n"
        arrows_init += "]\n"

    customization = {
        "labelx": spec.get("labelx"),
        "labely": spec.get("labely"),
    }
    ordered_keys = ["figx", "figy", "ymin", "ymax", "xmin", "xmax", "ticksopt_x", "ticksopt_y"]
    skip_keys = {"experiments", "labels", "showplot", "plotCag", "labelx", "labely"}
    for key in ordered_keys + [k for k in kwargs if k not in ordered_keys]:
        if key in kwargs and key not in skip_keys:
            customization[key] = kwargs[key]
    plot_customization_str = "\n".join(
        f"    {k}={_format_script_value(v)}," for k, v in customization.items()
    )

    plot_init = f"plot = {plot_class.__name__}(\n"
    plot_init += "    experiments=exps,\n"
    plot_init += "    labels=labels,\n"
    if plot_class is AxionGagPlot:
        plot_init += f"    plotCag={kwargs.get('plotCag', False)},\n"
    # Arrows are added after building the plot, so show it at the end.
    plot_init += f"    showplot={not arrows},\n"
    plot_init += plot_customization_str
    plot_init += "\n)\n"
    if arrows:
        plot_init += "for x0, y0, x1, y1, arrow_options in arrows:\n"
        plot_init += "    plot.plot.add_patch(FancyArrowPatch((x0, y0), (x1, y1), **arrow_options))\n"
        plot_init += "plot.show_plot()\n"

    return imports + experiments_init + labels_init + arrows_init + plot_init


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
                "line_height_px": float(label.get("lineHeightPx", 0.0) or 0.0),
                "rotation_deg": float(label.get("rotationDeg", 0.0) or 0.0),
                "layer_width_px": float(label.get("layerWidth", 0.0) or 0.0),
                "layer_height_px": float(label.get("layerHeight", 0.0) or 0.0),
                "color": _normalize_css_color_for_mpl(
                    str(label.get("textColor", "black") or "black"),
                    default="black",
                ),
                "extra": label.get("mplExtra") or {},
            }
        )
    return labels_mpl


def get_mpl_arrows_from_browser_snapshot(arrows_snapshot):
    """Convert synced browser arrows (layer fractions, y from top) to figure fractions."""
    arrows_mpl = []
    for arrow in arrows_snapshot or []:
        try:
            arrows_mpl.append(
                {
                    "x0": float(arrow["x0"]),
                    "y0": 1.0 - float(arrow["y0"]),
                    "x1": float(arrow["x1"]),
                    "y1": 1.0 - float(arrow["y1"]),
                    "color": arrow.get("color", "#000000"),
                    "lw": arrow.get("lw", 1.0),
                    "arrowstyle": arrow.get("arrowstyle", "-|>"),
                    "mutation_scale": arrow.get("mutation_scale", 12.0),
                }
            )
        except (KeyError, TypeError, ValueError):
            continue
    return arrows_mpl


def get_experiments_from_selection(selected_rows, row_data):
    """Experiments dict from the grid selection.

    The selection can also be {"ids": [...]} right after it is set by a callback
    (script import), before the grid reports the selected rows back.
    """
    if isinstance(selected_rows, dict):
        rows_by_name = {row.get("name"): row for row in row_data or []}
        selected_rows = [
            rows_by_name[name] for name in selected_rows.get("ids", []) if name in rows_by_name
        ]
    exps = {}
    for row in selected_rows or []:
        exps[row["name"]] = row.copy()
    return exps


def resolve_axis_range(slider_value, exact_limits, axis):
    """Axis limits from the slider (log10), or the exact imported ones if unchanged."""
    if exact_limits and [round(v, 2) for v in slider_value] == exact_limits.get(f"{axis}_log"):
        return tuple(exact_limits[f"{axis}range"])
    return (10 ** slider_value[0], 10 ** slider_value[1])


def slider_marks(vmin, vmax):
    step = 2 if vmax - vmin <= 30 else 5
    return {i: str(i) for i in range(int(vmin), int(vmax) + 1, step)}


def run_script_importer(script_bytes):
    """Run script_importer.py on a script in a subprocess and return its result."""
    with tempfile.TemporaryDirectory(prefix="axlim-import-") as tmpdir:
        script_path = Path(tmpdir) / "imported_script.py"
        script_path.write_bytes(script_bytes)
        output_path = Path(tmpdir) / "import_result.json"
        env = dict(os.environ, MPLBACKEND="Agg")
        try:
            proc = subprocess.run(
                [sys.executable, str(SCRIPT_IMPORTER), str(script_path), str(output_path)],
                cwd=tmpdir,
                env=env,
                capture_output=True,
                text=True,
                timeout=SCRIPT_IMPORT_TIMEOUT_S,
            )
        except subprocess.TimeoutExpired:
            return {
                "ok": False,
                "error": f"The script took more than {SCRIPT_IMPORT_TIMEOUT_S} s to run.",
            }
        if not output_path.exists():
            error = (proc.stderr or proc.stdout or "Unknown error").strip()
            return {"ok": False, "error": error[-3000:]}
        return json.loads(output_path.read_text())


def build_overlay_labels(labels, figsize, layer_size, dpi):
    """Draggable overlay labels from imported labels (inverse of the Apply conversion).

    Imported positions are the top-left corner of each text in figure fractions.
    """
    figx, figy = figsize
    layer_w = float((layer_size or {}).get("width") or 0) or DEFAULT_LAYER_WIDTH_PX
    layer_h = layer_w * figy / figx
    scale = figx * dpi / layer_w  # figure px per overlay px

    children = []
    for label in labels:
        font_px = label["fontsize_pt"] * dpi / 72.0 / LABEL_FONT_SCALE_CORRECTION / scale
        top_leading_px = (
            (LABEL_CSS_LINE_HEIGHT - 1.0) * font_px * 0.5 * LABEL_VERTICAL_OFFSET_TUNE
        )
        rotation_deg = -float(label.get("rotation_deg", 0.0))  # CSS rotates clockwise
        theta = math.radians(rotation_deg)
        left = label["x_frac"] * layer_w + math.sin(theta) * top_leading_px
        top = (1.0 - label["y_frac"]) * layer_h - math.cos(theta) * top_leading_px
        extra = label.get("extra") or {}
        children.append(
            html.Div(
                label["text"],
                className="draggable-label",
                style={
                    "textAlign": extra.get("multialignment") or extra.get("ma") or "left",
                    "left": f"{left:.4f}px",
                    "top": f"{top:.4f}px",
                    "color": label.get("color", "#000000"),
                    "fontSize": f"{font_px:.4f}px",
                    "transform": f"rotate({rotation_deg}deg)",
                    "transformOrigin": "top left",
                },
                **{
                    "data-rotation-deg": f"{rotation_deg}",
                    "data-mpl-extra": json.dumps(extra),
                },
            )
        )
    return children


def get_imported_extra_kwargs(plot_type, constructor_kwargs):
    """Imported constructor options that differ from what the app would use."""
    defaults = get_app_default_constructor_kwargs(plot_type)
    extra = {}
    for key, value in (constructor_kwargs or {}).items():
        if key == "excludedRegionOptions":
            if value:
                extra[key] = value
        elif defaults.get(key) != value:
            extra[key] = value
    return extra

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dag.themes.QUARTZ])
app.title = "Interactive Plotter"

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
        dcc.Store(id="arrows-dom-store", data=[]),
        dcc.Store(id="arrows-import-store"),
        dcc.Store(id="arrows-load-ack"),
        dcc.Store(id="layer-size-store"),
        dcc.Store(id="plot-extra-kwargs", data={}),
        dcc.Store(id="exact-limits"),
        dcc.Interval(id="labels-sync-interval", interval=300, n_intervals=0),
        html.H1(
            "Interactive Plotter",
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
                        html.Div(
                            style={
                                "display": "flex",
                                "alignItems": "center",
                                "gap": "8px",
                                "marginBottom": "10px",
                            },
                            children=[
                                dcc.Dropdown(
                                    id="plot-type-selector",
                                    options=plot_options,
                                    #value=plot_options[0]['value'],  # Set a default value
                                    placeholder="Select a Plot Type",
                                    searchable=False,
                                    style={"flex": "1"},
                                    className="dark-theme",
                                ),
                                html.Span(
                                    "Figure size (in):",
                                    style={"color": "#dfe4ff", "fontSize": "14px"},
                                ),
                                dcc.Input(
                                    id="figx-input",
                                    type="number",
                                    min=2,
                                    max=30,
                                    step=0.1,
                                    value=PLOT_TYPE_DEFAULTS["AxionGag"]["figsize"][0],
                                    debounce=True,
                                    className="figsize-input",
                                ),
                                html.Span("×", style={"color": "#dfe4ff"}),
                                dcc.Input(
                                    id="figy-input",
                                    type="number",
                                    min=2,
                                    max=30,
                                    step=0.1,
                                    value=PLOT_TYPE_DEFAULTS["AxionGag"]["figsize"][1],
                                    debounce=True,
                                    className="figsize-input",
                                ),
                            ],
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
                                        html.Div(
                                            id="arrows-layer",
                                            className="arrows-layer",
                                            **{"data-fig-dpi": f"{mpl.rcParams['figure.dpi']}"},
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
                                "alignItems": "center",
                                "flexWrap": "wrap",
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
                                    "Add Arrow",
                                    id="btn-add-arrow",
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
                                    "Apply Labels & Arrows",
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
                                html.Div(
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "gap": "8px",
                                        "color": "#dfe4ff",
                                        "fontSize": "14px",
                                    },
                                    children=[
                                        html.Span("Color:"),
                                        html.Div(
                                            id="label-color-palette",
                                            style={
                                                "display": "flex",
                                                "gap": "6px",
                                                "alignItems": "center",
                                            },
                                            children=[
                                                html.Button(
                                                    "",
                                                    className="label-color-swatch",
                                                    style={"backgroundColor": c},
                                                    **{"data-color": c},
                                                )
                                                for c in [
                                                    "#000000",
                                                    "#ffffff",
                                                    "#ff0404",
                                                    "#ffee00",
                                                    "#08fc00",
                                                    "#0314fc",
                                                    "#f708e3",
                                                    "#fa8f04",
                                                ]
                                            ],
                                        ),
                                        html.Button(
                                            "More colors",
                                            id="btn-label-color-more",
                                            style={
                                                "backgroundColor": "#3f4b63",
                                                "color": "white",
                                                "padding": "6px 10px",
                                                "border": "1px solid #64748b",
                                                "cursor": "pointer",
                                                "borderRadius": "6px",
                                                "fontSize": "13px",
                                            },
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        # Filled by assets/draggable_arrows.js
                        html.Div(id="arrow-toolbar", style={"marginTop": "10px"}),
                        html.Div(
                            children=[
                                html.Div(
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "gap": "10px",
                                    },
                                    children=[
                                        dcc.Dropdown(
                                            id="ticksopt-x-selector",
                                            options=[
                                                {"label": "normal", "value": "normal"},
                                                {"label": "dense", "value": "dense"},
                                            ],
                                            value="normal",
                                            clearable=False,
                                            searchable=False,
                                            style={"width": "120px"},
                                            className="dark-theme",
                                        ),
                                        html.Div(
                                            style={"flex": "1"},
                                            children=[
                                                dcc.RangeSlider(
                                                    id="x-range-slider",
                                                    min=-15, max=15, step=0.01,
                                                    marks={i: str(i) for i in range(-15, 16, 2)},
                                                    value=[-11, 9],
                                                    tooltip={"placement": "bottom", "always_visible": True},
                                                    className="dark-theme",
                                                ),
                                            ],
                                        ),
                                    ],
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
                                html.Div(
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "gap": "10px",
                                    },
                                    children=[
                                        dcc.Dropdown(
                                            id="ticksopt-y-selector",
                                            options=[
                                                {"label": "normal", "value": "normal"},
                                                {"label": "dense", "value": "dense"},
                                            ],
                                            value="normal",
                                            clearable=False,
                                            searchable=False,
                                            style={"width": "120px"},
                                            className="dark-theme",
                                        ),
                                        html.Div(
                                            style={"flex": "1"},
                                            children=[
                                                dcc.RangeSlider(
                                                    id="y-range-slider",
                                                    min=-20, max=5, step=0.01,
                                                    marks={i: str(i) for i in range(-20, 6, 2)},
                                                    value=[-18, -4],
                                                    tooltip={"placement": "bottom", "always_visible": True},
                                                    className="dark-theme",
                                                ),
                                            ],
                                        ),
                                    ],
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
                            getRowId="params.data.name",
                            className="ag-theme-quartz-dark",
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
                                    style={"marginRight": "20px"},
                                ),
                                # Import an existing plotting script
                                dcc.Upload(
                                    id="upload-script",
                                    accept=".py",
                                    multiple=False,
                                    children=html.Button(
                                        "Import script 📂",
                                        style={
                                            "backgroundColor": "#3f4b63",
                                            "color": "white",
                                            "padding": "10px 24px",
                                            "border": "none",
                                            "cursor": "pointer",
                                            "borderRadius": "5px",
                                            "fontSize": "24px",
                                        },
                                    ),
                                ),
                            ],
                        ),
                        dcc.Loading(html.Div(id="import-status"), type="dot"),
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

app.clientside_callback(
    ClientsideFunction(namespace="arrows", function_name="snapshot"),
    Output("arrows-dom-store", "data"),
    Input("labels-sync-interval", "n_intervals"),
)

app.clientside_callback(
    ClientsideFunction(namespace="overlay", function_name="layerSize"),
    Output("layer-size-store", "data"),
    Input("labels-sync-interval", "n_intervals"),
)

app.clientside_callback(
    ClientsideFunction(namespace="arrows", function_name="load"),
    Output("arrows-load-ack", "data"),
    Input("arrows-import-store", "data"),
    prevent_initial_call=True,
)

# Callbacks
@app.callback(
    Output("curve-plot", "src"),
    Input("x-range-slider", "value"),
    Input("y-range-slider", "value"),
    Input("ticksopt-x-selector", "value"),
    Input("ticksopt-y-selector", "value"),
    Input("ag-grid", "selectedRows"),
    Input("ag-grid", "cellValueChanged"),
    Input("plot-type-selector", "value"),
    Input("figx-input", "value"),
    Input("figy-input", "value"),
    Input("plot-extra-kwargs", "data"),
    State("exact-limits", "data"),
    State("ag-grid", "rowData"),
)
def update_plot_axis_ranges(
    x_range,
    y_range,
    ticksopt_x,
    ticksopt_y,
    selected_curves,
    cell_changed,
    plot_type,
    figx,
    figy,
    extra_kwargs,
    exact_limits,
    row_data,
):
    print("selected curves en el callback", selected_curves)
    exps = get_experiments_from_selection(selected_curves, row_data)
    return create_plot(
        experiments=exps,
        xrange=resolve_axis_range(x_range, exact_limits, "x"),
        yrange=resolve_axis_range(y_range, exact_limits, "y"),
        plot_type=plot_type,
        ticksopt_x=ticksopt_x or "normal",
        ticksopt_y=ticksopt_y or "normal",
        figx=figx,
        figy=figy,
        extra_kwargs=extra_kwargs,
    )

# change plot type (sliders ranges, database, figure size) or import a script
@app.callback(
    Output("plot-type-selector", "value"),
    Output("x-range-slider", "min"),
    Output("x-range-slider", "max"),
    Output("x-range-slider", "value"),
    Output("x-range-slider", "marks"),
    Output("y-range-slider", "min"),
    Output("y-range-slider", "max"),
    Output("y-range-slider", "value"),
    Output("y-range-slider", "marks"),
    Output("ag-grid", "rowData"),
    Output("ag-grid", "selectedRows"),
    Output("ticksopt-x-selector", "value"),
    Output("ticksopt-y-selector", "value"),
    Output("figx-input", "value"),
    Output("figy-input", "value"),
    Output("labels-layer", "children", allow_duplicate=True),
    Output("arrows-import-store", "data"),
    Output("plot-extra-kwargs", "data"),
    Output("exact-limits", "data"),
    Output("import-status", "children"),
    Output("upload-script", "contents"),
    Input("plot-type-selector", "value"),
    Input("upload-script", "contents"),
    State("upload-script", "filename"),
    State("layer-size-store", "data"),
    prevent_initial_call="initial_duplicate",
)
def update_plot_type_or_import(plot_type, script_contents, script_filename, layer_size):
    if ctx.triggered_id == "upload-script":
        return import_plotting_script(script_contents, script_filename, layer_size)

    defaults = PLOT_TYPE_DEFAULTS.get(plot_type, PLOT_TYPE_DEFAULTS["AxionGag"])
    x_min, x_max, x_value = defaults["x"]
    y_min, y_max, y_value = defaults["y"]
    figx, figy = defaults["figsize"]
    return (
        no_update,
        x_min, x_max, x_value, slider_marks(x_min, x_max),
        y_min, y_max, y_value, slider_marks(y_min, y_max),
        select_database(plot_type),
        no_update,
        no_update,
        no_update,
        figx,
        figy,
        no_update,
        no_update,
        {},
        None,
        no_update,
        no_update,
    )


def import_plotting_script(script_contents, script_filename, layer_size):
    """Outputs of update_plot_type_or_import for an uploaded plotting script."""
    n_outputs = 21
    if not script_contents:
        return (no_update,) * n_outputs

    def _status_only(status):
        return (no_update,) * (n_outputs - 2) + (status, None)

    try:
        script_bytes = base64.b64decode(script_contents.split(",", 1)[1])
        result = run_script_importer(script_bytes)
    except Exception as err:  # noqa: BLE001 - report any error in the app
        result = {"ok": False, "error": str(err)}
    if not result.get("ok"):
        return _status_only(
            html.Div(
                f"Could not import '{script_filename}':\n{result.get('error', '')}",
                className="import-error",
            )
        )

    plot_type = result["plot_type"]
    defaults = PLOT_TYPE_DEFAULTS[plot_type]

    def _slider(default, limits):
        vmin, vmax, _ = default
        value = [round(math.log10(v), 2) for v in limits]
        vmin = min(vmin, math.floor(value[0]))
        vmax = max(vmax, math.ceil(value[1]))
        return vmin, vmax, value, slider_marks(vmin, vmax)

    x_slider = _slider(defaults["x"], result["xlim"])
    y_slider = _slider(defaults["y"], result["ylim"])
    exact_limits = {
        "x_log": x_slider[2],
        "y_log": y_slider[2],
        "xrange": result["xlim"],
        "yrange": result["ylim"],
    }

    # Imported experiments first (in the script order) with their draw options,
    # followed by the rest of the database.
    db_rows = select_database(plot_type)
    rows_by_name = {row["name"]: row for row in db_rows}
    imported_rows = []
    n_custom = 0
    for name, experiment in result["experiments"].items():
        row = rows_by_name.pop(name, None)
        if row is None:
            row = {"name": name}
            n_custom += 1
        row.update(experiment)
        imported_rows.append(row)
    row_data = imported_rows + [row for row in db_rows if row["name"] in rows_by_name]
    selected = {"ids": list(result["experiments"].keys())}

    figx, figy = result["figsize"]
    labels_children = build_overlay_labels(
        result["labels"], (figx, figy), layer_size, mpl.rcParams["figure.dpi"]
    )
    arrows_import = {
        "arrows": [
            {**arrow, "y0": 1.0 - arrow["y0"], "y1": 1.0 - arrow["y1"]}
            for arrow in result["arrows"]
        ],
        "nonce": time.time(),
    }
    extra_kwargs = get_imported_extra_kwargs(plot_type, result.get("constructor_kwargs"))

    plot_label = next(
        (opt["label"] for opt in plot_options if opt["value"] == plot_type), plot_type
    )
    summary = (
        f"Imported '{script_filename}': {plot_label}, "
        f"{len(result['experiments'])} experiments"
        + (f" ({n_custom} not in the database)" if n_custom else "")
        + f", {len(result['labels'])} labels, {len(result['arrows'])} arrows."
    )
    if extra_kwargs:
        summary += " Kept script options: " + ", ".join(extra_kwargs) + "."
    warnings = result.get("warnings") or []
    status = html.Div(
        [html.Span(summary)]
        + ([html.Ul([html.Li(w) for w in warnings])] if warnings else [])
    )

    return (
        plot_type,
        *x_slider,
        *y_slider,
        row_data,
        selected,
        result.get("ticksopt_x", "normal"),
        result.get("ticksopt_y", "normal"),
        round(figx, 3),
        round(figy, 3),
        labels_children,
        arrows_import,
        extra_kwargs,
        exact_limits,
        status,
        None,
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
                "color": "#000000",
            },
        )
    )
    return labels


@app.callback(
    Output("curve-plot", "src", allow_duplicate=True),
    Input("btn-apply-labels", "n_clicks"),
    State("x-range-slider", "value"),
    State("y-range-slider", "value"),
    State("ticksopt-x-selector", "value"),
    State("ticksopt-y-selector", "value"),
    State("ag-grid", "selectedRows"),
    State("plot-type-selector", "value"),
    State("labels-dom-store", "data"),
    State("arrows-dom-store", "data"),
    State("figx-input", "value"),
    State("figy-input", "value"),
    State("plot-extra-kwargs", "data"),
    State("exact-limits", "data"),
    State("ag-grid", "rowData"),
    prevent_initial_call=True,
)
def apply_labels_to_current_plot(
    n_clicks,
    x_range,
    y_range,
    ticksopt_x,
    ticksopt_y,
    selected_curves,
    plot_type,
    labels_snapshot,
    arrows_snapshot,
    figx,
    figy,
    extra_kwargs,
    exact_limits,
    row_data,
):
    exps = get_experiments_from_selection(selected_curves, row_data)

    labels_mpl = get_mpl_labels_from_browser_snapshot(labels_snapshot)
    arrows_mpl = get_mpl_arrows_from_browser_snapshot(arrows_snapshot)
    return create_plot(
        experiments=exps,
        xrange=resolve_axis_range(x_range, exact_limits, "x"),
        yrange=resolve_axis_range(y_range, exact_limits, "y"),
        plot_type=plot_type,
        labels_mpl=labels_mpl,
        ticksopt_x=ticksopt_x or "normal",
        ticksopt_y=ticksopt_y or "normal",
        figx=figx,
        figy=figy,
        arrows_mpl=arrows_mpl,
        extra_kwargs=extra_kwargs,
    )

@app.callback(
    Output("download-py", "data"),
    Input("btn-generate-py", "n_clicks"),
    prevent_initial_call=True
)
def generate_python_file(n_clicks):
    if GENERATED_SPEC is None:
        return no_update
    # Contenido del archivo Python como un string
    python_code = generate_plotting_script_str(GENERATED_SPEC)
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
    app.run(debug=False)
