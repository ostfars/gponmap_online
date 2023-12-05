var map = new L.Map('map').setView([44.95792, 34.11026], 9);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

map.pm.addControls({
    position: 'topleft',
});
map.pm.setLang("ru");

//var geojsonLayer = L.geoJSON().addTo(map);

//var layers = L.PM.Utils.findLayers(map);

map.on('pm:create', function (e) {
    var layers = L.PM.Utils.findLayers(map)
    console.log(layers)
});

map.on('pm:remove', function (e) {
    var layers = L.PM.Utils.findLayers(map)
    console.log(layers)
});
//var group = L.featureGroup();
//layers.forEach((layer)=>{
//    group.addLayer(layer);
//});
//shapes = group.toGeoJSON();


//var newLayer = map.pm.getGeomanLayers(true).toGeoJSON();
//
//var layersAvailable = L.PM.Utils.findLayers(map);
//var group = L.featureGroup();
//layersAvailable.forEach((layer)=>{
//    group.addLayer(layer);
//});
//shapes = group.toGeoJSON();
//
//map.on('pm:create', function (e) {
//    console.log(layersAvailable)
//    console.log(layerGroup);
//});


