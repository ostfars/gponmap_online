//var map = L.map('map').setView([44.95792, 34.11026], 9);
//L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//    attribution: 'Map data &copy; OpenStreetMap contributors',
//    maxZoom: 20,
//}).addTo(map);

var osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 20,
    attribution: '© OpenStreetMap'
});

var otm = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: 'Map data: © OpenStreetMap contributors, SRTM | Map style: © OpenTopoMap (CC-BY-SA)'
});

var esri = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
    attribution: '© Esri'
});

var stamen = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.png', {
    attribution: 'Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'
});

var yandex = L.tileLayer(
  'http://vec{s}.maps.yandex.net/tiles?l=map&v=4.55.2&z={z}&x={x}&y={y}&scale=2&lang=ru_RU', {
    subdomains: ['01', '02', '03', '04'],
    attribution: '<a http="yandex.ru" target="_blank">Яндекс</a>',
    reuseTiles: true,
    updateWhenIdle: false
  }
);

var map = L.map('map', {
    center: [39.73, -104.99],
    zoom: 10,
    layers: [osm]
});

var baseMaps = {
    "OpenStreetMap": osm,
    "OpenTopoMap": otm,
    "ArcGIS": esri,
    "Yandex": yandex
};


var layerControl = L.control.layers(baseMaps).addTo(map);