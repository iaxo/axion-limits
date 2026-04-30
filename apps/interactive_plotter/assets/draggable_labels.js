(() => {
    let activeElement = null;
    let activeArrowHandle = null;
    let selectedElement = null;
    let shiftX = 0;
    let shiftY = 0;
    let colorButtons = [];

    const getClosest = (target, selector) => {
        if (!target) {
            return null;
        }
        if (typeof target.closest === "function") {
            return target.closest(selector);
        }
        const element = target.parentElement;
        return element && typeof element.closest === "function"
            ? element.closest(selector)
            : null;
    };

    const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

    const getNumericStylePx = (element, prop, fallback = 0) => {
        const raw = element && element.style ? element.style[prop] : "";
        const value = parseFloat(raw || "");
        return Number.isFinite(value) ? value : fallback;
    };

    const isLabel = (element) => element && element.classList.contains("draggable-label");
    const isArrow = (element) => element && element.classList.contains("draggable-arrow");

    const onPointerMove = (event) => {
        if (activeArrowHandle) {
            const { arrow, handleType, fixedX, fixedY } = activeArrowHandle;
            const layer = arrow.parentElement;
            if (!layer) {
                return;
            }

            const layerRect = layer.getBoundingClientRect();
            const pointer = getPointerInLayer(event, layerRect);
            const clamped = clampPointToLayer(pointer.x, pointer.y, layerRect);

            if (handleType === "start") {
                setArrowFromEndpoints(arrow, clamped.x, clamped.y, fixedX, fixedY);
            } else {
                setArrowFromEndpoints(arrow, fixedX, fixedY, clamped.x, clamped.y);
            }
            return;
        }

        if (!activeElement) {
            return;
        }

        const layer = activeElement.parentElement;
        if (!layer) {
            return;
        }

        const layerRect = layer.getBoundingClientRect();
        const itemRect = activeElement.getBoundingClientRect();

        const nextLeft = event.clientX - layerRect.left - shiftX;
        const nextTop = event.clientY - layerRect.top - shiftY;

        // For arrows, clamp by anchor point (left/top) so length does not block movement.
        const maxLeft = isArrow(activeElement)
            ? layerRect.width
            : layerRect.width - itemRect.width;
        const maxTop = isArrow(activeElement)
            ? layerRect.height
            : layerRect.height - itemRect.height;

        activeElement.style.left = `${clamp(nextLeft, 0, Math.max(0, maxLeft))}px`;
        activeElement.style.top = `${clamp(nextTop, 0, Math.max(0, maxTop))}px`;
    };

    const stopDragging = () => {
        if (!activeElement && !activeArrowHandle) {
            return;
        }

        if (activeElement) {
            activeElement.style.zIndex = "2";
        }
        if (activeArrowHandle && activeArrowHandle.arrow) {
            activeArrowHandle.arrow.style.zIndex = "2";
        }

        activeElement = null;
        activeArrowHandle = null;
        document.body.style.userSelect = "";
    };

    const getElementColor = (element) => {
        const value = (element && element.style && element.style.color) || "";
        return value && value.trim() ? value : "#000000";
    };

    const setSwatchesEnabled = (enabled) => {
        colorButtons.forEach((btn) => {
            btn.disabled = !enabled;
            btn.classList.toggle("disabled", !enabled);
        });
    };

    const selectElement = (element) => {
        selectedElement = element || null;
        document
            .querySelectorAll(".draggable-label.selected, .draggable-arrow.selected")
            .forEach((el) => {
                el.classList.remove("selected");
            });

        if (!selectedElement) {
            setSwatchesEnabled(false);
            syncArrowStyleSelectorWithSelection();
            return;
        }

        selectedElement.classList.add("selected");
        setSwatchesEnabled(true);
        syncArrowStyleSelectorWithSelection();
    };

    const getRotationDeg = (element) => {
        const value = parseFloat(element.dataset.rotationDeg || "0");
        return Number.isFinite(value) ? value : 0;
    };

    const setRotationDeg = (element, rotationDeg) => {
        element.dataset.rotationDeg = `${rotationDeg}`;
        if (isLabel(element)) {
            element.style.transform = `rotate(${rotationDeg}deg)`;
            element.style.transformOrigin = "top left";
            return;
        }
        if (isArrow(element)) {
            element.style.transform = `translateY(-50%) rotate(${rotationDeg}deg)`;
            element.style.transformOrigin = "left center";
        }
    };

    const setArrowLengthPx = (arrow, lengthPx) => {
        const nextLength = Math.max(lengthPx, 1);
        arrow.dataset.lengthPx = `${nextLength}`;
        arrow.style.width = `${nextLength}px`;
    };

    const setArrowLineWidthPx = (arrow, lineWidthPx) => {
        const nextWidth = clamp(lineWidthPx, 1, 8);
        arrow.dataset.lineWidthPx = `${nextWidth}`;
        arrow.style.borderTopWidth = `${nextWidth}px`;
    };

    const setArrowHeadWidthPx = (arrow, headWidthPx) => {
        const nextWidth = clamp(headWidthPx, 6, 36);
        arrow.dataset.headWidthPx = `${nextWidth}`;
        arrow.style.setProperty("--arrow-head-width-px", `${nextWidth}px`);
    };

    const setArrowStyle = (arrow, arrowStyle) => {
        const nextStyle = (arrowStyle || "-|>").toString();
        arrow.dataset.arrowStyle = nextStyle;
    };

    const getArrowHeadStyleSelector = () =>
        document.getElementById("arrow-head-style-selector");

    const syncArrowStyleSelectorWithSelection = () => {
        const selector = getArrowHeadStyleSelector();
        if (!selector) {
            return;
        }

        if (!selectedElement || !isArrow(selectedElement)) {
            selector.disabled = true;
            return;
        }

        selector.disabled = false;
        selector.value = selectedElement.dataset.arrowStyle || "-|>";
    };

    const getArrowLengthPx = (arrow) =>
        parseFloat(arrow.dataset.lengthPx || arrow.style.width || "80") || 80;

    const getArrowEndpoints = (arrow) => {
        const startX = getNumericStylePx(arrow, "left", 0);
        const startY = getNumericStylePx(arrow, "top", 0);
        const rotationDeg = getRotationDeg(arrow);
        const lengthPx = getArrowLengthPx(arrow);
        const theta = (rotationDeg * Math.PI) / 180;
        return {
            startX,
            startY,
            endX: startX + Math.cos(theta) * lengthPx,
            endY: startY + Math.sin(theta) * lengthPx,
        };
    };

    const setArrowFromEndpoints = (arrow, startX, startY, endX, endY) => {
        const dx = endX - startX;
        const dy = endY - startY;
        const lengthPx = Math.hypot(dx, dy);
        const rotationDeg = (Math.atan2(dy, dx) * 180) / Math.PI;

        arrow.style.left = `${startX}px`;
        arrow.style.top = `${startY}px`;
        setArrowLengthPx(arrow, lengthPx);
        setRotationDeg(arrow, rotationDeg);
    };

    const clampPointToLayer = (x, y, layerRect) => ({
        x: clamp(x, 0, Math.max(0, layerRect.width)),
        y: clamp(y, 0, Math.max(0, layerRect.height)),
    });

    const getPointerInLayer = (event, layerRect) => ({
        x: event.clientX - layerRect.left,
        y: event.clientY - layerRect.top,
    });

    const ensureArrowHandles = (arrow) => {
        if (!arrow || !isArrow(arrow)) {
            return;
        }
        if (arrow.querySelector(".arrow-handle-start") && arrow.querySelector(".arrow-handle-end")) {
            return;
        }

        const startHandle = document.createElement("span");
        startHandle.className = "arrow-handle arrow-handle-start";
        startHandle.dataset.handle = "start";
        arrow.appendChild(startHandle);

        const endHandle = document.createElement("span");
        endHandle.className = "arrow-handle arrow-handle-end";
        endHandle.dataset.handle = "end";
        arrow.appendChild(endHandle);
    };

    const ensureAllArrowHandles = () => {
        document.querySelectorAll(".draggable-arrow").forEach(ensureArrowHandles);
    };

    const finishEdit = (label) => {
        if (!label || !label.classList.contains("editing")) {
            return;
        }
        const text = (label.textContent || "").trim();
        label.textContent = text || "Label";
        label.contentEditable = "false";
        label.spellcheck = false;
        label.classList.remove("editing");
    };

    const startEdit = (label) => {
        if (!label || label.classList.contains("editing")) {
            return;
        }
        stopDragging();
        label.dataset.originalText = label.textContent || "";
        label.contentEditable = "true";
        label.spellcheck = false;
        label.classList.add("editing");
        label.focus();

        const selection = window.getSelection();
        if (!selection) {
            return;
        }
        const range = document.createRange();
        range.selectNodeContents(label);
        range.collapse(false);
        selection.removeAllRanges();
        selection.addRange(range);
    };

    document.addEventListener("pointerdown", (event) => {
        const arrowHandle = getClosest(event.target, ".arrow-handle");
        if (arrowHandle) {
            const arrow = getClosest(arrowHandle, ".draggable-arrow");
            if (!arrow) {
                return;
            }

            selectElement(arrow);
            if (!arrow.dataset.rotationDeg) {
                setRotationDeg(arrow, 0);
            }
            if (!arrow.dataset.lengthPx) {
                setArrowLengthPx(arrow, getNumericStylePx(arrow, "width", 80));
            }
            if (!arrow.dataset.lineWidthPx) {
                const width =
                    parseFloat(window.getComputedStyle(arrow).borderTopWidth || "2") || 2;
                setArrowLineWidthPx(arrow, width);
            }
            if (!arrow.dataset.headWidthPx) {
                setArrowHeadWidthPx(arrow, 10);
            }
            if (!arrow.dataset.arrowStyle) {
                setArrowStyle(arrow, "-|>");
            }

            const endpoints = getArrowEndpoints(arrow);
            if (arrowHandle.dataset.handle === "start") {
                activeArrowHandle = {
                    arrow,
                    handleType: "start",
                    fixedX: endpoints.endX,
                    fixedY: endpoints.endY,
                };
            } else {
                activeArrowHandle = {
                    arrow,
                    handleType: "end",
                    fixedX: endpoints.startX,
                    fixedY: endpoints.startY,
                };
            }

            arrow.style.zIndex = "3";
            document.body.style.userSelect = "none";
            event.preventDefault();
            return;
        }

        const element = getClosest(
            event.target,
            ".draggable-label, .draggable-arrow"
        );
        if (!element) {
            const paletteClick = getClosest(event.target, ".label-color-swatch");
            const moreColorsClick = getClosest(event.target, "#btn-label-color-more");
            if (!paletteClick && !moreColorsClick) {
                selectElement(null);
            }
            return;
        }

        if (isLabel(element) && element.classList.contains("editing")) {
            return;
        }

        selectElement(element);

        const layer = element.parentElement;
        if (!layer) {
            return;
        }
        const layerRect = layer.getBoundingClientRect();
        const currentLeft = getNumericStylePx(element, "left", 0);
        const currentTop = getNumericStylePx(element, "top", 0);

        shiftX = event.clientX - (layerRect.left + currentLeft);
        shiftY = event.clientY - (layerRect.top + currentTop);
        activeElement = element;

        if (!element.dataset.rotationDeg) {
            setRotationDeg(element, 0);
        }
        if (isArrow(element)) {
            ensureArrowHandles(element);
            if (!element.dataset.lengthPx) {
                setArrowLengthPx(element, getNumericStylePx(element, "width", 80));
            }
            if (!element.dataset.lineWidthPx) {
                const width =
                    parseFloat(window.getComputedStyle(element).borderTopWidth || "2") || 2;
                setArrowLineWidthPx(element, width);
            }
            if (!element.dataset.headWidthPx) {
                setArrowHeadWidthPx(element, 10);
            }
            if (!element.dataset.arrowStyle) {
                setArrowStyle(element, "-|>");
            }
        }

        element.style.zIndex = "3";
        document.body.style.userSelect = "none";
    });

    document.addEventListener(
        "wheel",
        (event) => {
            const element = getClosest(
                event.target,
                ".draggable-label, .draggable-arrow"
            );
            if (!element) {
                return;
            }
            if (isLabel(element) && element.classList.contains("editing")) {
                return;
            }

            event.preventDefault();

            if (event.shiftKey) {
                if (isArrow(element)) {
                    const currentHeadWidth =
                        parseFloat(element.dataset.headWidthPx || "10") || 10;
                    const nextHeadWidth = currentHeadWidth + (event.deltaY > 0 ? -1 : 1);
                    setArrowHeadWidthPx(element, nextHeadWidth);
                    return;
                }

                const currentRotation = getRotationDeg(element);
                const nextRotation = currentRotation + (event.deltaY > 0 ? 2 : -2);
                setRotationDeg(element, nextRotation);
                return;
            }

            if (isLabel(element)) {
                const currentFontPx =
                    parseFloat(window.getComputedStyle(element).fontSize || "13") || 13;
                const nextFontPx = Math.min(
                    72,
                    Math.max(6, currentFontPx + (event.deltaY > 0 ? -1 : 1))
                );
                element.style.fontSize = `${nextFontPx}px`;
                return;
            }

            if (isArrow(element)) {
                const currentLineWidth =
                    parseFloat(element.dataset.lineWidthPx || element.style.borderTopWidth || "2") || 2;
                const nextLineWidth = currentLineWidth + (event.deltaY > 0 ? -0.5 : 0.5);
                setArrowLineWidthPx(element, nextLineWidth);
            }
        },
        { passive: false }
    );

    document.addEventListener("dblclick", (event) => {
        const label = getClosest(event.target, ".draggable-label");
        if (!label) {
            return;
        }
        startEdit(label);
    });

    document.addEventListener("keydown", (event) => {
        const label = getClosest(event.target, ".draggable-label.editing");
        if (!label) {
            return;
        }

        if (event.key === "Enter") {
            event.preventDefault();
            finishEdit(label);
            label.blur();
            return;
        }

        if (event.key === "Escape") {
            event.preventDefault();
            label.textContent = label.dataset.originalText || "Label";
            finishEdit(label);
            label.blur();
        }
    });

    document.addEventListener(
        "blur",
        (event) => {
            const label = getClosest(event.target, ".draggable-label.editing");
            if (!label) {
                return;
            }
            finishEdit(label);
        },
        true
    );

    document.addEventListener("pointermove", onPointerMove);
    document.addEventListener("pointerup", stopDragging);
    document.addEventListener("pointercancel", stopDragging);

    const initColorPicker = () => {
        ensureAllArrowHandles();
        colorButtons = Array.from(document.querySelectorAll(".label-color-swatch"));
        if (colorButtons.length) {
            setSwatchesEnabled(!!selectedElement);
        }

        const arrowHeadStyleSelector = getArrowHeadStyleSelector();
        if (arrowHeadStyleSelector && !arrowHeadStyleSelector.dataset.boundChangeListener) {
            arrowHeadStyleSelector.addEventListener("change", (event) => {
                const targetArrow =
                    (selectedElement && isArrow(selectedElement) ? selectedElement : null) ||
                    document.querySelector(".draggable-arrow.selected");
                if (!targetArrow) {
                    return;
                }
                setArrowStyle(targetArrow, event.target.value || "-|>");
            });
            arrowHeadStyleSelector.dataset.boundChangeListener = "1";
        }

        syncArrowStyleSelectorWithSelection();
    };

    document.addEventListener("click", (event) => {
        const swatch = getClosest(event.target, ".label-color-swatch");
        if (!swatch) {
            return;
        }

        event.preventDefault();
        const targetElement =
            selectedElement ||
            document.querySelector(".draggable-label.selected, .draggable-arrow.selected");
        if (!targetElement) {
            return;
        }

        const color = swatch.dataset.color || "#000000";
        targetElement.style.color = color;
        selectedElement = targetElement;
    });

    document.addEventListener("click", (event) => {
        const moreColorsButton = getClosest(event.target, "#btn-label-color-more");
        if (!moreColorsButton) {
            return;
        }

        event.preventDefault();
        const targetElement =
            selectedElement ||
            document.querySelector(".draggable-label.selected, .draggable-arrow.selected");
        if (!targetElement) {
            return;
        }

        const nativePicker = document.createElement("input");
        nativePicker.type = "color";
        nativePicker.value = getElementColor(targetElement);
        nativePicker.style.position = "fixed";
        nativePicker.style.left = "-9999px";
        nativePicker.style.top = "-9999px";
        document.body.appendChild(nativePicker);

        const applyAndCleanup = () => {
            targetElement.style.color = nativePicker.value || "#000000";
            nativePicker.remove();
        };
        nativePicker.addEventListener("input", applyAndCleanup, { once: true });
        nativePicker.addEventListener("change", applyAndCleanup, { once: true });
        nativePicker.click();
    });

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initColorPicker, { once: true });
    } else {
        initColorPicker();
    }

    const observeLayerMutations = () => {
        const layer = document.getElementById("labels-layer");
        if (!layer) {
            return;
        }
        const observer = new MutationObserver(() => {
            ensureAllArrowHandles();
        });
        observer.observe(layer, { childList: true, subtree: true });
    };

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", observeLayerMutations, { once: true });
    } else {
        observeLayerMutations();
    }
})();

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    labels: {
        snapshot: function (nIntervals) {
            const layer = document.getElementById("labels-layer");
            if (!layer) {
                return [[], []];
            }

            const layerRect = layer.getBoundingClientRect();
            const labels = Array.from(layer.querySelectorAll(".draggable-label"));
            const arrows = Array.from(layer.querySelectorAll(".draggable-arrow"));

            const labelsSnapshot = labels.map((label) => {
                const labelRect = label.getBoundingClientRect();
                const computedStyle = window.getComputedStyle(label);
                const fontSizePx = parseFloat(computedStyle.fontSize || "13") || 13;
                const lineHeightPx =
                    parseFloat(computedStyle.lineHeight || "") || fontSizePx * 1.2;
                return {
                    text: (label.textContent || "").trim(),
                    left: parseFloat(label.style.left || "0") || 0,
                    top: parseFloat(label.style.top || "0") || 0,
                    width: labelRect.width,
                    height: labelRect.height,
                    fontSizePx,
                    lineHeightPx,
                    rotationDeg: parseFloat(label.dataset.rotationDeg || "0") || 0,
                    textColor: computedStyle.color || label.style.color || "#000000",
                    layerWidth: layerRect.width,
                    layerHeight: layerRect.height,
                };
            });

            const arrowsSnapshot = arrows.map((arrow) => {
                const computedStyle = window.getComputedStyle(arrow);
                return {
                    left: parseFloat(arrow.style.left || "0") || 0,
                    top: parseFloat(arrow.style.top || "0") || 0,
                    lengthPx: parseFloat(arrow.dataset.lengthPx || arrow.style.width || "80") || 80,
                    lineWidthPx:
                        parseFloat(arrow.dataset.lineWidthPx || computedStyle.borderTopWidth || "2") || 2,
                    headWidthPx: parseFloat(arrow.dataset.headWidthPx || "10") || 10,
                    arrowStyle: arrow.dataset.arrowStyle || "-|>",
                    rotationDeg: parseFloat(arrow.dataset.rotationDeg || "0") || 0,
                    color: computedStyle.color || arrow.style.color || "#000000",
                    layerWidth: layerRect.width,
                    layerHeight: layerRect.height,
                };
            });

            return [labelsSnapshot, arrowsSnapshot];
        },
    },
});
