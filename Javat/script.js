
//TO DO
//hacer que con los inputs X e Y solo se desplace una unidad, arriba abajo derecha o ezquierda
//Hacer que el input de texto permita reconocer latex.
//Cuando descarga el pdf no se le aplica el cambio de fuente.



document.addEventListener('DOMContentLoaded', function() {
const draggableContainer = d3.select("#draggableContainer");
const textInput = d3.select("#textInput");
const xInput = d3.select("#xInput");
const yInput = d3.select("#yInput");

const rotationInput = d3.select("#rotationInput");
const sizeInput = d3.select("#sizeInput");
const fontInput = d3.select("#fontInput");
const colorInput = d3.select("#colorInput");

const createButton = d3.select("#createButton");
const svgInput = d3.select("#svgInput");
const svgContainer = d3.select("#svgContainer");

let isDragging = false;
let offsetX, offsetY;
let draggingElement = null;
let initialX, initialY;
const createdTextElements = [];

function createDraggable(text) {
  
  const draggable = svgContainer.append("g")
    .attr("class", "draggable")
    .attr("transform", "translate(50, 50)");

  const textElement = draggable.append("text")
    .attr("x", 0)
    .attr("y", 0)
    .attr("text-anchor", "middle")
    .attr("dominant-baseline", "middle")
    .text("");

  // Restablecer los valores de los campos de entrada
  textInput.node().value = "";
  rotationInput.node().value = 0;
  sizeInput.node().value = 15;
  colorInput.node().value = "#000000";
  // Initialize font size
  const initialFontSize = 15; // You can set a default value
  textElement.style("font-size", initialFontSize);
  // Initialize font family
  const initialFontFamily = "Arial"; // You can set a default value
  textElement.style("font-family", initialFontFamily);
  //Initialize Color
  const initialTextColor = "#000000"; // Default black color
  textElement.style("fill", initialTextColor);
  
  draggable.on("mousedown", function(e) {
    isDragging = true;
    draggingElement = this;
    const point = svgContainer.node().createSVGPoint();
    point.x = e.clientX;
    point.y = e.clientY;
    const transformedPoint = point.matrixTransform(svgContainer.node().getScreenCTM().inverse());
    offsetX = transformedPoint.x - parseFloat(this.getAttribute("transform").split("(")[1]);
    offsetY = transformedPoint.y - parseFloat(this.getAttribute("transform").split(",")[1]);
    initialX = e.clientX;
    initialY = e.clientY;
    d3.select(this).style("cursor", "grabbing");

  });

  d3.select(document).on("mousemove", function(e) {
    if (!isDragging) return;
    const point = svgContainer.node().createSVGPoint();
    point.x = e.clientX;
    point.y = e.clientY;
    const transformedPoint = point.matrixTransform(svgContainer.node().getScreenCTM().inverse());
    var x = transformedPoint.x - offsetX;
    var y = transformedPoint.y - offsetY;
    // Update X and Y input values
    document.getElementById("xInput").value = x;
    document.getElementById("yInput").value = y;
    updateTable();
    // Update X and Y inputs in real-time
    const deltaX = e.clientX - initialX;
    const deltaY = e.clientY - initialY;
    draggingElement.setAttribute("transform", `translate(${x}, ${y})`);
    initialX += deltaX;
    initialY += deltaY;

  
    const rotation = -rotationInput.node().value;
    textElement.attr("transform", `rotate(${rotation})`);
  });

  d3.select(document).on("mouseup", function() {
    isDragging = false;
    draggingElement.style.cursor = "grab";
    draggingElement = null;
  });


  textElement.on("dblclick", function() {
    const index = createdTextElements.findIndex(elem => elem.textElement.node() === this);
    if (index !== -1) {
      const selectedTextElement = createdTextElements[index];
      textInput.node().value = selectedTextElement.initialText;
      rotationInput.node().value = selectedTextElement.initialRotation;
      sizeInput.node().value = selectedTextElement.initialFontSize;
      fontInput.node().value = selectedTextElement.initialFontFamily;
      colorInput.node().value = selectedTextElement.initialTextColor
      // Establecer el elemento actualmente editado
      draggingElement = selectedTextElement.textElement.node();
      d3.select(draggingElement).style("cursor", "grabbing");
    }
  });
    // Agregar evento de entrada de texto para actualizar el contenido del elemento de texto
  textInput.on("input", function() {
      const newText = this.value;
      textElement.text(newText);
      const index = createdTextElements.findIndex(elem => elem.textElement.node() === textElement.node());
      if (index !== -1) {
        createdTextElements[index].initialText = newText;

      }
        // Elimina la clase "editing" del elemento draggable
    draggingElement.classList.remove("editing");
    });
    // Agregar evento de entrada de texto para actualizar el contenido de la rotacion
  rotationInput.on("input", function() {
    const rotation = -rotationInput.node().value;
    textElement.attr("transform", `rotate(${rotation})`);

    const index = createdTextElements.findIndex(elem => elem.textElement.node() === textElement.node());
    if (index !== -1) {
      createdTextElements[index].initialRotation = rotation;

    }
  });
  xInput.on("input", function() {
    const newX = +xInput.node().value;
    const index = createdTextElements.findIndex(elem => elem.textElement.node() === textElement.node());
  
    if (index !== -1) {
      // Actualiza el valor de traslación en X
      createdTextElements[index].textElement.attr("transform", `translate(${newX}, ${0})`);
      console.log("me muevo",newX, " en el eje X");
      updateTable();
    }
  });
  
  yInput.on("input", function() {
    const newY = +yInput.node().value;
    const index = createdTextElements.findIndex(elem => elem.textElement.node() === textElement.node());
  
    if (index !== -1) {
      // Actualiza el valor de traslación en Y
      createdTextElements[index].textElement.attr("transform", `translate(${0}, ${newY})`);
      updateTable();
    }
  });
  
  //agregar evento para el tamaño
  sizeInput.on("input", function() {
    const fontSize = sizeInput.node().value;
    textElement.style("font-size", fontSize + "px");

    const index = createdTextElements.findIndex(elem => elem.textElement.node() === textElement.node());
    if (index !== -1) {
      createdTextElements[index].initialFontSize = fontSize;

    }
  });
  //agregar el evento para el tipo de fuente
  fontInput.on("change", function() {
    const fontFamily = fontInput.node().value;
    textElement.style("font-family", fontFamily);

    const index = createdTextElements.findIndex(elem => elem.textElement.node() === textElement.node());
    if (index !== -1) {
      createdTextElements[index].initialFontFamily = fontFamily;

    }
  });
  // agregar eventar para seleccion de color del texto
    
  colorInput.on("input", function() {
    const textColor = colorInput.node().value;
    textElement.style("fill", textColor);

    const index = createdTextElements.findIndex(elem => elem.textElement.node() === textElement.node());
    if (index !== -1) {
      createdTextElements[index].initialTextColor = textColor;

    }
  });

  // Store the text element and its properties
    createdTextElements.push({
      textElement: textElement,
      initialText: text,
      initialX: 50,
      initialY: 50,
      initialRotation: 0,
      initialFontSize: initialFontSize,
      initialFontFamily: initialFontFamily,
      initialTextColor: initialTextColor
    });
    
    return { draggable, textElement }; // Devuelve el elemento arrastrable y su elemento de texto

  }

  function loadSvg() {
    const file = svgInput.node().files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function(event) {
        const svgString = event.target.result;
        svgContainer.html(svgString);

        const loadedSvg = svgContainer.select('svg');
        const svgWidth = loadedSvg.attr('width');
        const svgHeight = loadedSvg.attr('height');
        svgContainer.attr('width', svgWidth).attr('height', svgHeight); // Ajustar dimensiones del contenedor

        };
      reader.readAsText(file);
    }
  }

  //Eventos
  createButton.on("click", function() {
    // Crear un elemento arrastrable sin texto inicial
    const { draggable, textElement } = createDraggable();
    selectedTextElement.draggable.classed("editing", true);


    // Restablecer los valores de los campos de entrada
    textInput.node().value = "";
    rotationInput.node().value = 0;
    sizeInput.node().value = 15;
    fontInput.node().value = "Arial";
    colorInput.node().value = "#000000";
    xInput.node().value = 50;
    yInput.node().value = 50;
  });

  svgInput.on("change", loadSvg);

  document.getElementById('createButton').addEventListener('click', addRow);

  function addRow() {
    const table = document.getElementById('textTable');
    const newRow = table.insertRow();

    newRow.classList.add('editable-row');

    const values = [
        document.getElementById('textInput').value,
        document.getElementById('xInput').value,
        document.getElementById('yInput').value,
        document.getElementById('sizeInput').value,
        document.getElementById('rotationInput').value,
        document.getElementById('colorInput').value,
        document.getElementById('fontInput').value
    ];

    for (let i = 0; i < values.length; i++) {
        const cell = newRow.insertCell(i);
        cell.textContent = values[i];
        cell.classList.add(`${['name', 'x', 'y', 'size', 'rotation', 'color', 'font'][i]}-input`);
    }

    const newRowInputs = newRow.querySelectorAll('input');
    newRowInputs.forEach(input => {
        input.addEventListener('input', function() {
            updateRow(newRow);
        });
    });

    lastAddedRow = newRow;

  }

  // Añadir los event listeners para los campos de entrada después de que el documento esté listo
    document.getElementById('textInput').addEventListener('input', updateTable);
    document.getElementById('xInput').addEventListener('input', updateTable);
    document.getElementById('yInput').addEventListener('input', updateTable);
    document.getElementById('sizeInput').addEventListener('input', updateTable);
    document.getElementById('rotationInput').addEventListener('input', updateTable);
    document.getElementById('colorInput').addEventListener('input', updateTable);
    document.getElementById('fontInput').addEventListener('input', updateTable);
  

  function updateTable() {
      if (lastAddedRow) {
          const cells = lastAddedRow.cells;
          cells[0].textContent = document.getElementById('textInput').value;
          cells[1].textContent = parseInt(document.getElementById('xInput').value);
          cells[2].textContent = parseInt(document.getElementById('yInput').value);
          cells[3].textContent = document.getElementById('sizeInput').value;
          cells[4].textContent = document.getElementById('rotationInput').value;
          cells[5].textContent = document.getElementById('colorInput').value;
          cells[6].textContent = document.getElementById('fontInput').value;
    }
}

document.getElementById('downloadDataBtn').addEventListener('click', function() {
  const table = document.getElementById('textTable');
  const rows = table.querySelectorAll('tr.editable-row');

  let txtContent = "Name, X, Y, size, Rotation, Color, Font\n"; // Encabezados

  rows.forEach(row => {
    const cells = row.cells;
    const rowData = Array.from(cells).map(cell => cell.textContent).join(', ');
    txtContent += rowData + '\n';
  });

  // Eliminar el último salto de línea si no es necesario
  txtContent = txtContent.trimRight();

  // Solicitar al usuario el nombre deseado del archivo (sin la extensión)
  const fileNameWithoutExtension = prompt("Ingresa el nombre deseado para el archivo (sin la extensión):", "tabla");
  if (!fileNameWithoutExtension) return; // Si el usuario cancela, no hacer nada

  // Agregar la extensión ".txt" al nombre proporcionado por el usuario
  const fileName = fileNameWithoutExtension + ".txt";

  // Crear un Blob con el contenido del archivo de texto
  const blob = new Blob([txtContent], { type: 'text/plain' });

  // Crear una URL de objeto local para el Blob
  const url = URL.createObjectURL(blob);

  // Crear un enlace de descarga
  const a = document.createElement('a');
  a.href = url;
  a.download = fileName; // Usar el nombre proporcionado por el usuario
  a.textContent = 'Descargar archivo';

  // Simular el clic en el enlace para iniciar la descarga
  a.click();

  // Liberar la URL de objeto local
  URL.revokeObjectURL(url);
});




function drawTextOnSVG(name, x, y, size, rotation, color, font) {
  const draggable = svgContainer.append("g")
      .attr("class", "draggable")
      .attr("transform", `translate(${x}, ${y})`);

  const textElement = draggable.append("text")
      .attr("x", 0)
      .attr("y", 0)
      .attr("text-anchor", "middle")
      .attr("dominant-baseline", "middle")
      .text(name)
      .style("font-size", size + "px")
      .style("fill", color)
      .style("font-family", font)
      .attr("transform", `rotate(${-rotation})`);

  // Store the text element and its properties
  createdTextElements.push({
      textElement: textElement,
      initialText: name,
      initialX: x,
      initialY: y,
      initialRotation: rotation,
      initialFontSize: size,
      initialFontFamily: font,
      initialTextColor: color
  });

  // Agregar fila a la tabla
  const table = document.getElementById('textTable');
  const newRow = table.insertRow();
  newRow.classList.add('editable-row');
  const values = [name, x, y, size, rotation, color, font];

  for (let i = 0; i < values.length; i++) {
      const cell = newRow.insertCell(i);
      cell.textContent = values[i];
      cell.classList.add(`${['name', 'x', 'y', 'size', 'rotation', 'color', 'font'][i]}-input`);
  }

  const newRowInputs = newRow.querySelectorAll('input');
  newRowInputs.forEach(input => {
      input.addEventListener('input', function() {
          updateRow(newRow);
      });
  });

  lastAddedRow = newRow;
}
document.getElementById('loadTxtInput').addEventListener('change', function(event) {
  const file = event.target.files[0];
  if (file) {
      const reader = new FileReader();
      reader.onload = function(event) {
          const fileContent = event.target.result;
          const lines = fileContent.split('\n');
          lines.shift(); // Ignorar la primera línea (encabezados)
          lines.forEach(line => {
              const [name, x, y, size, rotation, color, font] = line.split(', ');
              drawTextOnSVG(name, +x, +y, +size, +rotation, color, font);
          });
      };
      reader.readAsText(file);
  }
});

function downloadSVG() {
  const svgString = new XMLSerializer().serializeToString(svgContainer.node());
  const blob = new Blob([svgString], { type: "image/svg+xml" });

  const fileNameWithoutExtension = prompt("Ingresa el nombre deseado para el archivo SVG:", "modified");
  if (!fileNameWithoutExtension) return;

  const fileName = fileNameWithoutExtension + ".svg";

  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = fileName;
  a.textContent = "Descargar SVG";

  a.click();
  URL.revokeObjectURL(url);
}


function downloadPDF() {
  const svgElement = document.getElementById("svgContainer");
  const svgString = new XMLSerializer().serializeToString(svgElement);
  const svgWidth = svgElement.getBoundingClientRect().width;
  const svgHeight = svgElement.getBoundingClientRect().height;

  const pdfWidth = svgWidth * 0.75; // Mantener el ancho del PDF igual al ancho del SVG
  const pdfHeight = svgHeight * 0.75; // Mantener el alto del PDF igual al alto del SVG

  const doc = new window.PDFDocument({ size: [pdfWidth, pdfHeight] });
  const chunks = [];

  doc.on("data", (chunk) => {
    chunks.push(chunk);
  });

  doc.on("end", () => {
    const pdfBlob = new Blob(chunks, {
      type: "application/pdf"
    });
    const blobUrl = URL.createObjectURL(pdfBlob);

    const fileNameWithoutExtension = prompt("Ingresa el nombre deseado para el archivo PDF:", "downloaded");
    if (!fileNameWithoutExtension) return;

    const fileName = fileNameWithoutExtension + ".pdf";

    const a = document.createElement("a");
    a.href = blobUrl;
    a.download = fileName;
    a.textContent = "Descargar PDF";

    a.click();
    URL.revokeObjectURL(blobUrl);
  });

  const scale = pdfWidth / svgWidth; // Calcular el factor de escala
  window.SVGtoPDF(doc, svgString, 0, 0, { width: pdfWidth, height: pdfHeight, scale: scale });
  doc.end();
}




  document.getElementById("downloadSvgBtn").addEventListener("click", function () {
    downloadSVG();
  });
  document.getElementById("downloadPdfBtn").addEventListener("click", function () {
    downloadPDF();
  });



});
