(() => {
    // Shared state between the overlay modules (labels and arrows).
    const overlay = (window.axlimOverlay = window.axlimOverlay || {});

    const SVG_NS = "http://www.w3.org/2000/svg";
    const ARROW_STYLES = ["-", "->", "-|>", "<-", "<|-", "<->", "<|-|>"];
    const DEFAULT_ARROW = {
        color: "#000000",
        lw: 1.0,
        arrowstyle: "-|>",
        mutation_scale: 12,
    };
    // Same proportions as matplotlib's arrow styles (head_length=0.4, head_width=0.2).
    const HEAD_LENGTH = 0.4;
    const HEAD_HALF_WIDTH = 0.2;

    // Arrow positions are stored as fractions of the overlay layer (y from top),
    // which is the whole matplotlib figure, so they survive window resizes.
    let arrows = [];
    let nextId = 1;
    let selectedId = null;
    let drag = null;
    let toolbar = null;

    const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

    const getClosest = (target, selector) => {
        if (!target) {
            return null;
        }
        const element = typeof target.closest === "function" ? target : target.parentElement;
        return element && typeof element.closest === "function"
            ? element.closest(selector)
            : null;
    };

    const getLayer = () => document.getElementById("arrows-layer");

    const getSelected = () => arrows.find((a) => a.id === selectedId) || null;

    // CSS px of the overlay per matplotlib point.
    const pxPerPoint = (layer) => {
        const dpi = parseFloat(layer.dataset.figDpi || "100") || 100;
        const img = document.getElementById("curve-plot");
        const layerWidth = layer.clientWidth || 1;
        const scale = img && img.naturalWidth ? img.naturalWidth / layerWidth : 1;
        return dpi / 72 / scale;
    };

    const ensureSvg = () => {
        const layer = getLayer();
        if (!layer) {
            return null;
        }
        let svg = layer.querySelector("svg.arrows-svg");
        if (!svg) {
            svg = document.createElementNS(SVG_NS, "svg");
            svg.setAttribute("class", "arrows-svg");
            layer.appendChild(svg);
            if (typeof ResizeObserver === "function") {
                new ResizeObserver(() => render()).observe(layer);
            }
        }
        return svg;
    };

    const svgEl = (tag, attrs) => {
        const el = document.createElementNS(SVG_NS, tag);
        Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, `${v}`));
        return el;
    };

    const headPath = (tip, from, length, halfWidth, filled) => {
        const dx = tip.x - from.x;
        const dy = tip.y - from.y;
        const norm = Math.hypot(dx, dy) || 1;
        const ux = dx / norm;
        const uy = dy / norm;
        const bx = tip.x - ux * length;
        const by = tip.y - uy * length;
        const p1 = `${bx - uy * halfWidth},${by + ux * halfWidth}`;
        const p2 = `${bx + uy * halfWidth},${by - ux * halfWidth}`;
        return `M ${p1} L ${tip.x},${tip.y} L ${p2}${filled ? " Z" : ""}`;
    };

    const render = () => {
        const svg = ensureSvg();
        if (!svg) {
            return;
        }
        const layer = svg.parentElement;
        const width = layer.clientWidth;
        const height = layer.clientHeight;
        const ptPx = pxPerPoint(layer);

        while (svg.firstChild) {
            svg.removeChild(svg.firstChild);
        }

        arrows.forEach((arrow) => {
            const p0 = { x: arrow.x0 * width, y: arrow.y0 * height };
            const p1 = { x: arrow.x1 * width, y: arrow.y1 * height };
            const strokeWidth = Math.max(arrow.lw * ptPx, 0.5);
            const headLength = HEAD_LENGTH * arrow.mutation_scale * ptPx;
            const headHalfWidth = HEAD_HALF_WIDTH * arrow.mutation_scale * ptPx;

            const group = svgEl("g", { class: "overlay-arrow", "data-arrow-id": arrow.id });
            if (arrow.id === selectedId) {
                group.classList.add("selected");
            }

            const lineAttrs = { x1: p0.x, y1: p0.y, x2: p1.x, y2: p1.y };
            group.appendChild(svgEl("line", { ...lineAttrs, class: "arrow-hit" }));
            group.appendChild(
                svgEl("line", {
                    ...lineAttrs,
                    class: "arrow-shaft",
                    stroke: arrow.color,
                    "stroke-width": strokeWidth,
                })
            );

            const style = arrow.arrowstyle;
            const [startPart, endPart] = style === "-" ? ["", ""] : style.split("-");
            const heads = [
                { part: endPart, tip: p1, from: p0 },
                { part: startPart, tip: p0, from: p1 },
            ];
            heads.forEach(({ part, tip, from }) => {
                if (!part) {
                    return;
                }
                const filled = part.includes("|");
                group.appendChild(
                    svgEl("path", {
                        class: "arrow-head",
                        d: headPath(tip, from, headLength, headHalfWidth, filled),
                        stroke: arrow.color,
                        "stroke-width": strokeWidth,
                        "stroke-linejoin": "miter",
                        fill: filled ? arrow.color : "none",
                    })
                );
            });

            if (arrow.id === selectedId) {
                [p0, p1].forEach((p, end) => {
                    group.appendChild(
                        svgEl("circle", {
                            class: "arrow-handle",
                            cx: p.x,
                            cy: p.y,
                            r: 5,
                            "data-end": end,
                        })
                    );
                });
            }
            svg.appendChild(group);
        });
    };

    // --- toolbar -------------------------------------------------------------
    const buildToolbar = () => {
        const container = document.getElementById("arrow-toolbar");
        if (!container) {
            return null;
        }
        if (toolbar && toolbar.container === container) {
            return toolbar;
        }

        container.innerHTML = "";
        const addLabeled = (text, control) => {
            const wrapper = document.createElement("label");
            wrapper.className = "arrow-control";
            wrapper.style.display = "flex";
            wrapper.style.alignItems = "center";
            wrapper.style.gap = "4px";
            wrapper.appendChild(document.createTextNode(text));
            wrapper.appendChild(control);
            container.appendChild(wrapper);
            return control;
        };

        const title = document.createElement("span");
        title.textContent = "Arrow:";
        container.appendChild(title);

        const width = document.createElement("input");
        width.type = "number";
        width.min = "0.1";
        width.max = "20";
        width.step = "0.1";
        width.value = `${DEFAULT_ARROW.lw}`;
        width.title = "Line width (pt)";
        addLabeled("width", width);

        const style = document.createElement("select");
        style.title = "Arrow head style";
        ARROW_STYLES.forEach((s) => {
            const option = document.createElement("option");
            option.value = s;
            option.textContent = s === "-" ? "- (no head)" : s;
            style.appendChild(option);
        });
        style.value = DEFAULT_ARROW.arrowstyle;
        addLabeled("head", style);

        const head = document.createElement("input");
        head.type = "number";
        head.min = "1";
        head.max = "60";
        head.step = "1";
        head.value = `${DEFAULT_ARROW.mutation_scale}`;
        head.title = "Head size (pt)";
        addLabeled("head size", head);

        const remove = document.createElement("button");
        remove.type = "button";
        remove.textContent = "Delete arrow";
        remove.className = "arrow-control";
        container.appendChild(remove);

        const onChange = () => {
            const arrow = getSelected();
            if (!arrow) {
                return;
            }
            const lw = parseFloat(width.value);
            const ms = parseFloat(head.value);
            if (Number.isFinite(lw) && lw > 0) {
                arrow.lw = lw;
            }
            if (Number.isFinite(ms) && ms > 0) {
                arrow.mutation_scale = ms;
            }
            if (ARROW_STYLES.includes(style.value)) {
                arrow.arrowstyle = style.value;
            }
            render();
        };
        width.addEventListener("input", onChange);
        head.addEventListener("input", onChange);
        style.addEventListener("change", onChange);
        remove.addEventListener("click", () => deleteSelected());

        toolbar = { container, width, style, head, remove };
        return toolbar;
    };

    const refreshToolbar = () => {
        const tb = buildToolbar();
        if (!tb) {
            return;
        }
        const arrow = getSelected();
        const enabled = !!arrow;
        tb.container.classList.toggle("disabled", !enabled);
        [tb.width, tb.style, tb.head, tb.remove].forEach((el) => {
            el.disabled = !enabled;
        });
        if (arrow) {
            tb.width.value = `${arrow.lw}`;
            tb.style.value = arrow.arrowstyle;
            tb.head.value = `${arrow.mutation_scale}`;
        }
    };

    const selectArrow = (id) => {
        selectedId = id;
        refreshToolbar();
        render();
        if (typeof overlay.refreshSwatches === "function") {
            overlay.refreshSwatches();
        }
    };

    const deleteSelected = () => {
        if (selectedId === null) {
            return;
        }
        arrows = arrows.filter((a) => a.id !== selectedId);
        selectArrow(null);
    };

    const normalizeArrow = (data) => ({
        id: nextId++,
        x0: clamp(parseFloat(data.x0) || 0, 0, 1),
        y0: clamp(parseFloat(data.y0) || 0, 0, 1),
        x1: clamp(parseFloat(data.x1) || 0, 0, 1),
        y1: clamp(parseFloat(data.y1) || 0, 0, 1),
        color: data.color || DEFAULT_ARROW.color,
        lw: parseFloat(data.lw) > 0 ? parseFloat(data.lw) : DEFAULT_ARROW.lw,
        arrowstyle: ARROW_STYLES.includes(data.arrowstyle)
            ? data.arrowstyle
            : DEFAULT_ARROW.arrowstyle,
        mutation_scale:
            parseFloat(data.mutation_scale) > 0
                ? parseFloat(data.mutation_scale)
                : DEFAULT_ARROW.mutation_scale,
    });

    const addArrow = () => {
        const tb = buildToolbar();
        const offset = (arrows.length % 8) * 0.03;
        const arrow = normalizeArrow({
            x0: 0.35 + offset,
            y0: 0.6 + offset,
            x1: 0.55 + offset,
            y1: 0.4 + offset,
            color: DEFAULT_ARROW.color,
            lw: tb ? tb.width.value : DEFAULT_ARROW.lw,
            arrowstyle: tb ? tb.style.value : DEFAULT_ARROW.arrowstyle,
            mutation_scale: tb ? tb.head.value : DEFAULT_ARROW.mutation_scale,
        });
        arrows.push(arrow);
        selectArrow(arrow.id);
    };

    // --- shared API used by draggable_labels.js -----------------------------
    overlay.ensureReady = () => {
        const layer = getLayer();
        if (layer && !layer.querySelector("svg.arrows-svg")) {
            ensureSvg();
            render();
        }
        if (!toolbar || !document.body.contains(toolbar.container)) {
            refreshToolbar();
            if (typeof overlay.refreshSwatches === "function") {
                overlay.refreshSwatches();
            }
        }
    };
    overlay.hasSelectedArrow = () => selectedId !== null;
    overlay.deselectArrow = () => {
        if (selectedId !== null) {
            selectArrow(null);
        }
    };
    overlay.getSelectedArrowColor = () => {
        const arrow = getSelected();
        return arrow ? arrow.color : null;
    };
    overlay.setSelectedArrowColor = (color) => {
        const arrow = getSelected();
        if (!arrow) {
            return false;
        }
        arrow.color = color;
        render();
        return true;
    };
    overlay.setArrows = (list) => {
        arrows = (list || []).map(normalizeArrow);
        selectArrow(null);
    };
    overlay.getArrows = () =>
        arrows.map(({ x0, y0, x1, y1, color, lw, arrowstyle, mutation_scale }) => ({
            x0,
            y0,
            x1,
            y1,
            color,
            lw,
            arrowstyle,
            mutation_scale,
        }));

    // --- events ---------------------------------------------------------------
    document.addEventListener("pointerdown", (event) => {
        const group = getClosest(event.target, ".overlay-arrow");
        if (!group) {
            const keepSelection =
                getClosest(event.target, "#arrow-toolbar") ||
                getClosest(event.target, ".label-color-swatch") ||
                getClosest(event.target, "#btn-label-color-more");
            if (!keepSelection) {
                overlay.deselectArrow();
            }
            return;
        }

        const id = parseInt(group.dataset.arrowId, 10);
        const arrow = arrows.find((a) => a.id === id);
        const layer = getLayer();
        if (!arrow || !layer) {
            return;
        }
        event.preventDefault();
        if (selectedId !== id) {
            selectArrow(id);
        }

        const handle = getClosest(event.target, ".arrow-handle");
        drag = {
            arrow,
            end: handle ? parseInt(handle.dataset.end, 10) : null,
            startX: event.clientX,
            startY: event.clientY,
            initial: { x0: arrow.x0, y0: arrow.y0, x1: arrow.x1, y1: arrow.y1 },
        };
        document.body.style.userSelect = "none";
    });

    document.addEventListener("pointermove", (event) => {
        const layer = getLayer();
        if (!drag || !layer) {
            return;
        }
        const rect = layer.getBoundingClientRect();
        if (!rect.width || !rect.height) {
            return;
        }
        const { arrow, initial } = drag;
        if (drag.end === 0 || drag.end === 1) {
            const fx = clamp((event.clientX - rect.left) / rect.width, 0, 1);
            const fy = clamp((event.clientY - rect.top) / rect.height, 0, 1);
            arrow[`x${drag.end}`] = fx;
            arrow[`y${drag.end}`] = fy;
        } else {
            let dx = (event.clientX - drag.startX) / rect.width;
            let dy = (event.clientY - drag.startY) / rect.height;
            // keep the whole arrow inside the figure
            dx = clamp(dx, -Math.min(initial.x0, initial.x1), 1 - Math.max(initial.x0, initial.x1));
            dy = clamp(dy, -Math.min(initial.y0, initial.y1), 1 - Math.max(initial.y0, initial.y1));
            arrow.x0 = initial.x0 + dx;
            arrow.x1 = initial.x1 + dx;
            arrow.y0 = initial.y0 + dy;
            arrow.y1 = initial.y1 + dy;
        }
        render();
    });

    const stopDragging = () => {
        if (!drag) {
            return;
        }
        drag = null;
        document.body.style.userSelect = "";
    };
    document.addEventListener("pointerup", stopDragging);
    document.addEventListener("pointercancel", stopDragging);

    document.addEventListener("keydown", (event) => {
        if (selectedId === null || (event.key !== "Delete" && event.key !== "Backspace")) {
            return;
        }
        const target = event.target;
        const typing =
            target &&
            (target.isContentEditable ||
                ["INPUT", "TEXTAREA", "SELECT"].includes(target.tagName));
        if (typing) {
            return;
        }
        event.preventDefault();
        deleteSelected();
    });

    document.addEventListener("click", (event) => {
        if (getClosest(event.target, "#btn-add-arrow")) {
            event.preventDefault();
            addArrow();
        }
    });

    // Re-render when a new plot image is loaded (its pixel size may change).
    document.addEventListener(
        "load",
        (event) => {
            if (event.target && event.target.id === "curve-plot") {
                render();
            }
        },
        true
    );
    window.addEventListener("resize", render);

    const init = () => {
        ensureSvg();
        refreshToolbar();
    };
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init, { once: true });
    } else {
        init();
    }
})();

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    arrows: {
        snapshot: function (nIntervals) {
            const overlay = window.axlimOverlay || {};
            // The layout is rendered by Dash after this file loads: build the
            // svg layer and the toolbar as soon as their containers exist.
            if (typeof overlay.ensureReady === "function") {
                overlay.ensureReady();
            }
            return typeof overlay.getArrows === "function" ? overlay.getArrows() : [];
        },
        load: function (data) {
            const overlay = window.axlimOverlay || {};
            if (data && typeof overlay.setArrows === "function") {
                overlay.setArrows(data.arrows || []);
            }
            return null;
        },
    },
    overlay: {
        layerSize: function (nIntervals) {
            const layer = document.getElementById("labels-layer");
            if (!layer) {
                return window.dash_clientside.no_update;
            }
            const rect = layer.getBoundingClientRect();
            const size = { width: rect.width, height: rect.height };
            const key = `${size.width}x${size.height}`;
            if (key === window.axlimLastLayerSize) {
                return window.dash_clientside.no_update;
            }
            window.axlimLastLayerSize = key;
            return size;
        },
    },
});
