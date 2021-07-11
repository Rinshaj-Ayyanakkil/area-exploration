const addFloor = document.querySelector("#add-floor-button");
const floorContainer = document.querySelector('#floor-container');

let floorCount = 0;

let facilityMap = {};

wifiList.forEach(wifi => {
    const res = wifi[2].split('#');
    facilityMap.hasOwnProperty(res[0]) ? facilityMap[res[0]]++ : facilityMap[res[0]] = 1;
});

for (const key in facilityMap) {
    console.log(facilityMap[key])
    newFloor(facilityMap[key], key)
}

function newFloor(count, name) {
    const floor = document.createElement('div');
    floor.id = 'floor' + floorCount;
    floor.classList.add('floor');
    floor.innerText = name;
    floorContainer.appendChild(floor);
    floorContainer.insertBefore(floor, floorContainer.firstChild);
    floorCount++;
    for (let i = 0; i < count; i++)
        newHotspot(floor, i)
}

function newHotspot(floor, id) {
    // <i class="hotspot fa fa-wifi fa-2x" draggable="true"></i>
    const hotspot = document.createElement('div');
    hotspot.id = 'hotspot' + floorCount;
    hotspot.innerText = '#' + id;
    hotspot.classList.add('hotspot', 'fa', 'fa-wifi');
    hotspot.setAttribute('draggable', 'true')
    floor.appendChild(hotspot);
    floor.insertBefore(hotspot, floor.firstChild);
}

addFloor.addEventListener('click', () => {
    newFloor(0, nth(floorCount) + " floor")
});

let x = 0, y = 0;

const hotspots = document.querySelectorAll(".hotspot");
hotspots.forEach(hotspot => {

    hotspot.style.top = '300';
    hotspot.style.left = '400';

    hotspot.addEventListener('dragstart', () => {
        hotspot.classList.add('dragging')
    });

    hotspot.addEventListener('dragend', () => {
        hotspot.classList.remove('dragging')
    });
});


let nodeCount = 0;

function addNode(x, y) {
    const node = document.createElement('div');
    node.id = 'node' + nodeCount;
    node.classList.add('node', 'fa', 'fa-circle');
    node.style.left = x + "px";
    node.style.top = y + "px";
    document.body.appendChild(node);
    nodeCount++;
    const box = node.getBoundingClientRect();
    console.log(node.id + ":- " + "top:" + box.top + ", right: " + box.right + ", bottom: " + box.bottom + ", left: " + box.left);
}

const floors = document.querySelectorAll('.floor');
floors.forEach(floor => {
    floor.addEventListener('click', e => {
        addNode(e.pageX, e.pageY);
        const box = floor.getBoundingClientRect();
        console.log(floor.id + ":- " + "top:" + box.top + ", right: " + box.right + ", bottom: " + box.bottom + ", left: " + box.left);
    })
});

function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll('.hotspot:not(.dragging)')]

    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect()
        const offset = y - box.top - box.height / 2
        if (offset < 0 && offset > closest.offset) {
            return {offset: offset, element: child}
        } else {
            return closest
        }
    }, {offset: Number.NEGATIVE_INFINITY}).element
}

function nth(n) {
    return n === 1 ? '1st' : n === 2 ? '2nd' : n === 3 ? '3rd' : n + 'th';
}




