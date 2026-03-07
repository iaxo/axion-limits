(() => {
    let activeLabel = null;
    let shiftX = 0;
    let shiftY = 0;

    const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

    const onPointerMove = (event) => {
        if (!activeLabel) {
            return;
        }

        const layer = activeLabel.parentElement;
        if (!layer) {
            return;
        }

        const layerRect = layer.getBoundingClientRect();
        const labelRect = activeLabel.getBoundingClientRect();

        const nextLeft = event.clientX - layerRect.left - shiftX;
        const nextTop = event.clientY - layerRect.top - shiftY;

        const maxLeft = layerRect.width - labelRect.width;
        const maxTop = layerRect.height - labelRect.height;

        activeLabel.style.left = `${clamp(nextLeft, 0, Math.max(0, maxLeft))}px`;
        activeLabel.style.top = `${clamp(nextTop, 0, Math.max(0, maxTop))}px`;
    };

    const stopDragging = () => {
        if (!activeLabel) {
            return;
        }
        activeLabel.style.zIndex = "2";
        activeLabel = null;
        document.body.style.userSelect = "";
    };

    const getRotationDeg = (label) => {
        const value = parseFloat(label.dataset.rotationDeg || "0");
        return Number.isFinite(value) ? value : 0;
    };

    const setRotationDeg = (label, rotationDeg) => {
        label.dataset.rotationDeg = `${rotationDeg}`;
        label.style.transform = `rotate(${rotationDeg}deg)`;
        label.style.transformOrigin = "top left";
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
        const label = event.target.closest(".draggable-label");
        if (!label) {
            return;
        }
        if (label.classList.contains("editing")) {
            return;
        }

        const labelRect = label.getBoundingClientRect();
        shiftX = event.clientX - labelRect.left;
        shiftY = event.clientY - labelRect.top;
        activeLabel = label;

        if (!label.dataset.rotationDeg) {
            setRotationDeg(label, 0);
        }

        label.style.zIndex = "3";
        document.body.style.userSelect = "none";
    });

    document.addEventListener(
        "wheel",
        (event) => {
            const label = event.target.closest(".draggable-label");
            if (!label || label.classList.contains("editing")) {
                return;
            }

            event.preventDefault();

            if (event.shiftKey) {
                const currentRotation = getRotationDeg(label);
                const nextRotation = currentRotation + (event.deltaY > 0 ? 2 : -2);
                setRotationDeg(label, nextRotation);
                return;
            }

            const currentFontPx =
                parseFloat(window.getComputedStyle(label).fontSize || "13") || 13;
            const nextFontPx = Math.min(
                72,
                Math.max(6, currentFontPx + (event.deltaY > 0 ? -1 : 1))
            );
            label.style.fontSize = `${nextFontPx}px`;
        },
        { passive: false }
    );

    document.addEventListener("dblclick", (event) => {
        const label = event.target.closest(".draggable-label");
        if (!label) {
            return;
        }
        startEdit(label);
    });

    document.addEventListener("keydown", (event) => {
        const label = event.target.closest(".draggable-label.editing");
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
            const label = event.target.closest(".draggable-label.editing");
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
})();

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    labels: {
        snapshot: function (nIntervals) {
            const layer = document.getElementById("labels-layer");
            if (!layer) {
                return [];
            }

            const layerRect = layer.getBoundingClientRect();
            const labels = Array.from(layer.querySelectorAll(".draggable-label"));

            return labels.map((label) => {
                const labelRect = label.getBoundingClientRect();
                const computedStyle = window.getComputedStyle(label);
                return {
                    text: (label.textContent || "").trim(),
                    left: parseFloat(label.style.left || "0") || 0,
                    top: parseFloat(label.style.top || "0") || 0,
                    width: labelRect.width,
                    height: labelRect.height,
                    fontSizePx: parseFloat(computedStyle.fontSize || "13") || 13,
                    rotationDeg: parseFloat(label.dataset.rotationDeg || "0") || 0,
                    layerWidth: layerRect.width,
                    layerHeight: layerRect.height,
                };
            });
        },
    },
});
