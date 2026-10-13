var dagfuncs = (window.dashAgGridFunctions = window.dashAgGridFunctions || {});

// Clicking a row toggles its selection without clearing the other selected
// rows (the grid's default row click selects only the clicked row).
dagfuncs.toggleRowSelectionOnClick = function (params) {
    const field = params.colDef && params.colDef.field;
    // clicking the editable drawOptions cell is meant to edit it, not to select
    if (field === "drawOptions") {
        return;
    }
    // the checkbox already toggles the selection by itself
    const target = params.event && params.event.target;
    if (target && target.closest && target.closest(".ag-selection-checkbox")) {
        return;
    }
    params.node.setSelected(!params.node.isSelected());
};
