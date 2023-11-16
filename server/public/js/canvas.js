const canvas = document.getElementById("myCanvas");
const ctx = canvas.getContext('2d');

let canvasOffsetX = 0;
let canvasOffsetY = 0;

let color = "#000000";
let size = 5;
let prevColor = color;

let OnBrush = true;

let isPainting = false;
let startX = 0;
let startY = 0;

let drawingPaths = []; // Store the drawn paths as an array of points

resetCanvasSize();

const CanvasMover = document.getElementById('mover');
const canvasController = document.getElementById('canvas-controller');
controllerOffsetX = 0;
controllerOffsetY = 0;

function ToggleCanvasControl(e){
    const canvasController = document.getElementById('canvas-controller');
    const canvasControl = document.getElementById('canvas-control');
    canvasControl.classList.toggle('canvas-control-active')
    canvasController.classList.toggle('hide');
}

function moveCanvasController(e){
    // if move morethan screen width or height then return
    if (e.clientX + controllerOffsetX > window.innerWidth || e.clientY + controllerOffsetY > window.innerHeight) return;
    canvasController.style.left = `${e.clientX - controllerOffsetX}px`;
    canvasController.style.top = `${e.clientY - controllerOffsetY}px`;
}

function MakeAllChildNodeTo(NodeID, ClassName){
    const ParentNode = document.getElementById(NodeID);
    const ChildNode = ParentNode.childNodes;
    ChildNode.forEach(node => {
        if (node.classList.contains(ClassName)) return;
        node.classList.add(ClassName);
    });
}

CanvasMover.addEventListener('mousedown', e => {
    controllerOffsetX = e.clientX - canvasController.getBoundingClientRect().left;
    controllerOffsetY = e.clientY - canvasController.getBoundingClientRect().top;
    document.addEventListener('mousemove', moveCanvasController);
});

document.addEventListener('mouseup', e => {
    document.removeEventListener('mousemove', moveCanvasController);
});

const CanvasColor = document.getElementById('canvas-color');
CanvasColor.addEventListener('click', e => {
    const CanvasColorPicker = document.getElementById('canvas-color-picker');
    const ColorPreview = document.getElementById('color-preview');

    CanvasColorPicker.click();
    CanvasColorPicker.addEventListener('change', e => {
        OnBrush ? color = e.target.value : prevColor = e.target.value;
        ColorPreview.style.backgroundColor = e.target.value;
    });
});

const Eraser = document.getElementById('eraser');
Eraser.addEventListener('click', e => {
    OnBrush = false;
    prevColor = color;
    color = "#FFFFFF";
    // remove all active-brush classes
    let brush = document.querySelectorAll('.active-brush');
    brush.forEach(b => {
        b.classList.remove('active-brush');
    });
    Eraser.classList.add('active-brush');
});

const Brush = document.getElementById('brush');
Brush.addEventListener('click', e => {
    OnBrush = true;
    color = prevColor;
    // remove all active-brush classes
    let brush = document.querySelectorAll('.active-brush');
    brush.forEach(b => {
        b.classList.remove('active-brush');
    });
    Brush.classList.add('active-brush');
});

const thickness = document.getElementById('thickness');
thickness.addEventListener('click', e => {
    const thicknessPicker = document.getElementById('thickness-picker');
    const ToolsDropdown = document.getElementById('tools-dropdown');

    ToolsDropdown.classList.toggle('hide');
    // if tools-dropdown is alread shown then do nothing
    thicknessPicker.classList.toggle('hide')
    thicknessPicker.addEventListener('change', e => {
        document.querySelectorAll('.thickness-number').forEach(thick => {
            thick.innerHTML = e.target.value + 'px';
        });
        size = e.target.value;
    });
});

const ClearCanvas = document.getElementById('clear-canvas');
ClearCanvas.addEventListener('click', e => {
    ctx.fillStyle = "#FFFFFF";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    drawingPaths = [];
});

window.onresize = () => {
    resetCanvasSize();
}

canvas.addEventListener('mousedown', e => {
    isPainting = true;
    startX = e.clientX;
    startY = e.clientY;
    ctx.beginPath();
    drawingPaths.push([]); // Start a new path
    drawingPaths[drawingPaths.length - 1].push({ x: startX, y: startY }); // Add the starting point
});

canvas.addEventListener('mouseup', e => {
    if (isPainting) {
        isPainting = false;
    }
    ctx.stroke();
    ctx.beginPath();
});

canvas.addEventListener('mousemove', draw);

canvas.addEventListener('touchstart', e => {
    isPainting = true;
    startX = e.touches[0].clientX;
    startY = e.touches[0].clientY;
    ctx.beginPath();
    drawingPaths.push([]); // Start a new path
    drawingPaths[drawingPaths.length - 1].push({ x: startX, y: startY }); // Add the starting point
});

canvas.addEventListener('touchend', e => {
    if (isPainting) {
        isPainting = false;
        drawingPaths.push(null); // Add a null value to separate paths
    }
});

canvas.addEventListener('touchmove', drawtouch);

function drawtouch(e) {
    e.preventDefault();

    if (!isPainting) {
        return;
    }

    ctx.lineWidth = size;
    ctx.lineCap = 'round';
    ctx.strokeStyle = color;

    const x = e.touches[0].clientX - canvasOffsetX;
    const y = e.touches[0].clientY - canvasOffsetY;

    drawingPaths.push({ color, size, x, y });
    ctx.lineTo(x, y);
    ctx.stroke();
}

function draw(e) {
    if (!isPainting) {
        return;
    }

    ctx.lineWidth = size;
    ctx.lineCap = 'round';
    ctx.strokeStyle = color;

    const x = e.clientX - canvasOffsetX;
    const y = e.clientY - canvasOffsetY;

    drawingPaths.push({ color, size, x, y });
    ctx.lineTo(x, y);
    ctx.stroke();
}

function resetCanvasSize() {
    console.log("called")
    canvas.width = canvas.parentNode.offsetWidth;
    canvas.height = canvas.parentNode.offsetHeight;

    var viewportOffset = canvas.getBoundingClientRect();
    var top = viewportOffset.top;
    var left = viewportOffset.left;

    canvasOffsetX = left;
    canvasOffsetY = top;

    ctx.fillStyle = "#FFFFFF";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    redrawPaths(); // Redraw existing drawings after resizing
}

function redrawPaths() {
    
    ctx.lineCap = 'round';

    let previousPoint = null;

    drawingPaths.forEach(point => {
        ctx.strokeStyle = point.color;
        ctx.lineWidth = size;
        if (point === null) {
            previousPoint = null;
        } else {
            if (previousPoint) {
                ctx.beginPath();
                ctx.moveTo(previousPoint.x, previousPoint.y);
                ctx.lineTo(point.x, point.y);
                ctx.stroke();
            }
            previousPoint = point;
        }
    });
    ctx.stroke();
}