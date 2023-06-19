const copy = "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors";
const url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
const layer = L.tileLayer(url, { attribution: copy });
const map = L.map("map", { layers: [layer] });

//map.setView([44.95792, 34.11026], 9)
map.locate()
    .on("locationfound", (e) => map.setView(e.latlng, 16))
    .on("locationerror", () => map.setView([0, 0], 5));

async function load_gponmap() {
    const gponmap_url = `/api/gponmap/?in_bbox=${map
        .getBounds()
        .toBBoxString()}`;
    const response = await fetch(gponmap_url);
    const geojson = await response.json();
    return geojson;
}

async function render_gponmap() {
    const gponmap = await load_gponmap();
    L.geoJSON(gponmap)
        .bindPopup((layer) => layer.feature.properties.name)
        .addTo(map);
}

map.on("moveend", render_gponmap);
