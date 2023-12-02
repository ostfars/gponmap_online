var map = new L.Map('map').setView([44.95792, 34.11026], 9);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

map.pm.addControls({
    position: 'topleft',
});

map.pm.setLang("ru");

var geojsonLayer = L.geoJSON().addTo(map);

var newLayer = map.pm.getGeomanLayers(true).toGeoJSON();

var layersAvailable = L.PM.Utils.findLayers(map);

map.on('pm:create', function (e) {
    console.log(layersAvailable)
    console.log(newLayer);
});


