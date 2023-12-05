//to do:
//load kml
//convert to geoman
//change properties
//export kml
//upload to db

var map = new L.Map('map').setView([44.95792, 34.11026], 9);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

map.pm.addControls({
    position: 'topleft',
});
map.pm.setLang("ru");
