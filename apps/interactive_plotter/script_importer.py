"""Run an axionlimits plotting script in isolation and extract its plot state.

Usage:
    python script_importer.py <script.py> <output.json>

The script is executed as ``__main__`` with the axionlimits plot classes
instrumented at runtime (the package code is not modified):

- plot constructors are wrapped to record their (effective) arguments and to
  force ``showplot=False`` / ``saveplotname=None``;
- showing and saving figures is disabled, so the script writes no files.

After the script finishes, the state of the last plot created is written as
JSON to ``output.json``: plot type, axis limits, figure size, tick options,
experiments, labels and arrows (positions in figure fractions so that the app
can place them on its overlay), plus a list of warnings for anything that
could not be imported.

This module is meant to run in a subprocess (see ``import_script`` in app.py),
so the script cannot alter the app's global matplotlib state.
"""

import copy
import inspect
import json
import math
import runpy
import sys
import traceback

import matplotlib

matplotlib.use("Agg")

import matplotlib.colors as mcolors  # noqa: E402
import matplotlib.patheffects as mplpe  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import ArrowStyle, FancyArrowPatch  # noqa: E402
from matplotlib.text import Annotation, Text  # noqa: E402

from axionlimits.axion_plot import AxionGagPlot  # noqa: E402
from axionlimits.utils import custom_formatter, extract_kwargs  # noqa: E402
from axionlimits.wimp_plot import WimpPlot  # noqa: E402
from axionlimits.x_plotter import BasePlot  # noqa: E402

# Arrow styles the app overlay knows how to draw.
SUPPORTED_ARROWSTYLES = ["-", "->", "-|>", "<-", "<|-", "<->", "<|-|>"]

# Label kwargs that the overlay represents itself (position, size, colour,
# rotation, alignment); everything else is kept as "extra" mpl kwargs.
LABEL_KWARGS_HANDLED_BY_OVERLAY = {
    "x",
    "y",
    "s",
    "color",
    "c",
    "size",
    "fontsize",
    "rotation",
    "rotation_mode",
    "ha",
    "va",
    "horizontalalignment",
    "verticalalignment",
    "picker",
    "transform",
}

CAPTURED_PLOTS = []


def _is_jsonable(value):
    try:
        json.dumps(value)
    except (TypeError, ValueError):
        return False
    return True


def _to_hex(color, default="#000000"):
    try:
        return mcolors.to_hex(color, keep_alpha=False)
    except (TypeError, ValueError):
        return default


def _format_draw_options(draw_options):
    """Draw options as the string format understood by extract_kwargs."""
    if isinstance(draw_options, dict):
        return ", ".join(f"{k}={v!r}" for k, v in draw_options.items())
    if draw_options is None:
        return ""
    return str(draw_options)


# ------------------------------------------------------------------------------
# Runtime instrumentation
# ------------------------------------------------------------------------------
def _wrap_plot_init(cls):
    original_init = cls.__init__
    signature = inspect.signature(original_init)

    def wrapped_init(self, *args, **kwargs):
        bound = signature.bind(self, *args, **kwargs)
        bound.apply_defaults()
        arguments = {k: v for k, v in bound.arguments.items() if k != "self"}
        try:
            captured_kwargs = copy.deepcopy(arguments)
        except Exception:  # noqa: BLE001 - fall back to a shallow copy
            captured_kwargs = dict(arguments)

        bound.arguments["showplot"] = False
        bound.arguments["saveplotname"] = None
        original_init(*bound.args, **bound.kwargs)

        CAPTURED_PLOTS.append(
            {
                "plot": self,
                "cls": cls,
                "kwargs": captured_kwargs,
                "init_artist_ids": {id(a) for a in self.plot.get_children()},
                "n_init_texts": len(self.plot.texts),
            }
        )

    cls.__init__ = wrapped_init


def _instrument():
    _wrap_plot_init(AxionGagPlot)
    _wrap_plot_init(WimpPlot)

    def _noop(*_args, **_kwargs):
        return None

    BasePlot.show_plot = _noop
    BasePlot.save_plot = _noop
    plt.show = _noop
    plt.savefig = _noop
    Figure.savefig = _noop


# ------------------------------------------------------------------------------
# Extraction
# ------------------------------------------------------------------------------
def _get_plot_type(capture):
    if capture["cls"] is WimpPlot:
        return "WIMPSSI"
    if capture["kwargs"].get("plotCag", False):
        return "AxionCag"
    return "AxionGag"


def _get_experiments(capture):
    experiments = capture["kwargs"].get("experiments") or {}
    result = {}
    if not isinstance(experiments, dict):
        return result
    for name, info in experiments.items():
        info = info or {}
        exp = {
            "type": info.get("type", ""),
            "path": info.get("path", ""),
            "drawOptions": _format_draw_options(info.get("drawOptions", "")),
        }
        if "projection" in info:
            exp["projection"] = info["projection"]
        result[str(name)] = exp
    return result


def _text_top_left_display(text, renderer):
    """Top-left corner (in the text's own rotated frame) in display pixels.

    The axis-aligned extent of the rotated text box is centred on the box
    centre whatever ha/va/rotation_mode are, so the corner is the centre plus
    the rotated half-diagonal of the unrotated box.
    """
    extent = text.get_window_extent(renderer)
    cx = 0.5 * (extent.x0 + extent.x1)
    cy = 0.5 * (extent.y0 + extent.y1)

    rotation = text.get_rotation()
    text.set_rotation(0)
    unrotated = text.get_window_extent(renderer)
    text.set_rotation(rotation)
    half_w = 0.5 * unrotated.width
    half_h = 0.5 * unrotated.height

    theta = math.radians(rotation)
    dx = -half_w * math.cos(theta) - half_h * math.sin(theta)
    dy = -half_w * math.sin(theta) + half_h * math.cos(theta)
    return cx + dx, cy + dy


def _label_extras_from_kwargs(kwargs, warnings, label_text):
    extras = {}
    for key, value in (kwargs or {}).items():
        if key in LABEL_KWARGS_HANDLED_BY_OVERLAY:
            continue
        if not _is_jsonable(value):
            warnings.append(
                f"Label '{label_text}': option '{key}' could not be imported."
            )
            continue
        extras[key] = value
    return extras


def _label_extras_from_artist(text):
    extras = {}
    for pe in text.get_path_effects() or []:
        if isinstance(pe, mplpe.Stroke):
            extras["bc"] = _to_hex(pe._gc.get("foreground", "black"))
            extras["bw"] = pe._gc.get("linewidth", 1)
            break
    if text.get_fontweight() not in ("normal", 400):
        extras["fontweight"] = text.get_fontweight()
    if text.get_fontstyle() != "normal":
        extras["fontstyle"] = text.get_fontstyle()
    if text.get_alpha() is not None:
        extras["alpha"] = text.get_alpha()
    return extras


def _get_labels(capture, fig, renderer, warnings):
    ax = capture["plot"].plot
    fig_w, fig_h = fig.bbox.width, fig.bbox.height

    init_labels = capture["kwargs"].get("labels") or []
    n_init = capture["n_init_texts"]
    labels_match_init = len(init_labels) == n_init

    labels = []
    for i, text in enumerate(ax.texts):
        if not text.get_visible():
            continue
        raw_text = text.get_text()
        extras = None
        if labels_match_init and i < n_init:
            spec = init_labels[i]
            if isinstance(spec[0], str):
                raw_text = spec[0]
            spec_kwargs = spec[3] if len(spec) > 3 else {}
            if isinstance(spec_kwargs, str):
                spec_kwargs = extract_kwargs(spec_kwargs)
            if isinstance(spec_kwargs, dict):
                extras = _label_extras_from_kwargs(spec_kwargs, warnings, raw_text)
        if raw_text is None or not str(raw_text).strip():
            continue
        if extras is None:
            extras = _label_extras_from_artist(text)
        # Lines of a multi-line text are aligned like `ha` unless told otherwise;
        # keep that alignment as the label will be re-anchored with ha='left'.
        if "\n" in str(raw_text) and "ma" not in extras and "multialignment" not in extras:
            extras["multialignment"] = (
                text._multialignment or text.get_horizontalalignment()
            )

        x_disp, y_disp = _text_top_left_display(text, renderer)
        labels.append(
            {
                "text": str(raw_text),
                "x_frac": x_disp / fig_w,
                "y_frac": y_disp / fig_h,
                "fontsize_pt": float(text.get_fontsize()),
                # matplotlib reports rotations in [0, 360): use (-180, 180]
                "rotation_deg": -((-float(text.get_rotation()) + 180.0) % 360.0 - 180.0),
                "color": _to_hex(text.get_color()),
                "extra": extras,
            }
        )
    return labels


def _arrowstyle_name(style):
    """Map an ArrowStyle instance back to its short name."""
    if isinstance(style, str):
        return style
    for name, style_cls in ArrowStyle.get_styles().items():
        if type(style) is style_cls and name in SUPPORTED_ARROWSTYLES:
            return name
    return None


def _arrow_from_display(start, end, fig, **props):
    fig_w, fig_h = fig.bbox.width, fig.bbox.height
    arrow = {
        "x0": float(start[0]) / fig_w,
        "y0": float(start[1]) / fig_h,
        "x1": float(end[0]) / fig_w,
        "y1": float(end[1]) / fig_h,
    }
    arrow.update(props)
    return arrow


def _get_arrows(capture, fig, warnings):
    ax = capture["plot"].plot
    init_ids = capture["init_artist_ids"]
    arrows = []
    not_imported = {}

    for artist in ax.get_children():
        if id(artist) in init_ids or not artist.get_visible():
            continue

        if isinstance(artist, Annotation):
            patch = artist.arrow_patch
            if patch is None:
                continue  # plain text, handled as a label
            pos = getattr(patch, "_posA_posB", None)
            if not pos:
                not_imported["Annotation"] = not_imported.get("Annotation", 0) + 1
                continue
            arrowprops = artist.arrowprops or {}
            style = arrowprops.get("arrowstyle")
            style_name = style if style in SUPPORTED_ARROWSTYLES else None
            if style_name is None:
                warnings.append(
                    "Annotation arrow style not supported, imported as '-|>'."
                )
                style_name = "-|>"
            # Annotation arrows are positioned in display coordinates.
            start = patch.get_transform().transform(pos[0])
            end = patch.get_transform().transform(pos[1])
            arrows.append(
                _arrow_from_display(
                    start,
                    end,
                    fig,
                    color=_to_hex(patch.get_edgecolor()),
                    lw=float(patch.get_linewidth()),
                    arrowstyle=style_name,
                    mutation_scale=float(patch.get_mutation_scale()),
                )
            )
            continue

        if isinstance(artist, Text):
            continue  # labels are extracted separately

        if isinstance(artist, FancyArrowPatch):
            pos = getattr(artist, "_posA_posB", None)
            if not pos:
                not_imported["FancyArrowPatch"] = (
                    not_imported.get("FancyArrowPatch", 0) + 1
                )
                continue
            style_name = _arrowstyle_name(artist.get_arrowstyle())
            if style_name is None:
                warnings.append("Arrow style not supported, imported as '-|>'.")
                style_name = "-|>"
            transform = artist.get_transform()
            arrows.append(
                _arrow_from_display(
                    transform.transform(pos[0]),
                    transform.transform(pos[1]),
                    fig,
                    color=_to_hex(artist.get_edgecolor()),
                    lw=float(artist.get_linewidth()),
                    arrowstyle=style_name,
                    mutation_scale=float(artist.get_mutation_scale()),
                )
            )
            continue

        if isinstance(artist, Line2D):
            xy = artist.get_xydata()
            if len(xy) == 2 and artist.get_linestyle() not in ("None", "", " "):
                if artist.get_linestyle() != "-":
                    warnings.append(
                        "Line with non-solid linestyle imported as a solid arrow."
                    )
                transform = artist.get_transform()
                arrows.append(
                    _arrow_from_display(
                        transform.transform(xy[0]),
                        transform.transform(xy[1]),
                        fig,
                        color=_to_hex(artist.get_color()),
                        lw=float(artist.get_linewidth()),
                        arrowstyle="-",
                        mutation_scale=12.0,
                    )
                )
                continue

        name = type(artist).__name__
        not_imported[name] = not_imported.get(name, 0) + 1

    for name, count in not_imported.items():
        warnings.append(
            f"{count} element(s) of type {name} added after the plot "
            "constructor could not be imported."
        )
    return arrows


def _get_constructor_kwargs(capture, warnings):
    kwargs = capture["kwargs"]
    result = {}
    for key in ("labelx", "labely", "labelfontsize", "excludedRegion"):
        if key in kwargs and _is_jsonable(kwargs[key]):
            result[key] = kwargs[key]

    excluded_region_options = kwargs.get("excludedRegionOptions") or {}
    if excluded_region_options:
        if _is_jsonable(excluded_region_options):
            result["excludedRegionOptions"] = excluded_region_options
        else:
            warnings.append("Excluded region options could not be imported.")

    for key in ("tickformatter_x", "tickformatter_y"):
        if key in kwargs and kwargs[key] is not custom_formatter:
            warnings.append(f"Custom '{key}' is not supported and was ignored.")
    return result


def extract_state(capture, warnings):
    plot = capture["plot"]
    fig = plot.fig
    ax = plot.plot
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()

    kwargs = capture["kwargs"]
    return {
        "ok": True,
        "plot_class": capture["cls"].__name__,
        "plot_type": _get_plot_type(capture),
        "xlim": [float(v) for v in ax.get_xlim()],
        "ylim": [float(v) for v in ax.get_ylim()],
        "figsize": [float(v) for v in fig.get_size_inches()],
        "ticksopt_x": kwargs.get("ticksopt_x", "normal"),
        "ticksopt_y": kwargs.get("ticksopt_y", "normal"),
        "experiments": _get_experiments(capture),
        "labels": _get_labels(capture, fig, renderer, warnings),
        "arrows": _get_arrows(capture, fig, warnings),
        "constructor_kwargs": _get_constructor_kwargs(capture, warnings),
        "warnings": warnings,
    }


def run(script_path):
    _instrument()
    warnings = []
    script_error = None
    sys.argv = [script_path]
    try:
        runpy.run_path(script_path, run_name="__main__")
    except SystemExit:
        pass
    except Exception:  # noqa: BLE001 - report any script error to the app
        script_error = traceback.format_exc(limit=-3)  # frames of the script

    if not CAPTURED_PLOTS:
        message = "No AxionGagPlot or WimpPlot was created by the script."
        if script_error:
            message += "\n" + script_error
        return {"ok": False, "error": message}

    if script_error:
        warnings.append(
            "The script raised an error after creating the plot:\n" + script_error
        )
    if len(CAPTURED_PLOTS) > 1:
        warnings.append(
            f"The script created {len(CAPTURED_PLOTS)} plots; the last one was imported."
        )
    return extract_state(CAPTURED_PLOTS[-1], warnings)


def main():
    if len(sys.argv) != 3:
        sys.stderr.write(__doc__)
        sys.exit(2)
    script_path, output_path = sys.argv[1], sys.argv[2]
    try:
        result = run(script_path)
    except Exception:  # noqa: BLE001
        result = {"ok": False, "error": traceback.format_exc(limit=5)}
    with open(output_path, "w") as f:
        json.dump(result, f)


if __name__ == "__main__":
    main()
