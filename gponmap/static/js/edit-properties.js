var map = L.map('map').setView([44.95792, 34.11026], 9);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; OpenStreetMap contributors',
    maxZoom: 19,
}).addTo(map);

var geojsonLayer = L.geoJSON().addTo(map);

map.pm.addControls({
    position: 'topleft',
    drawCircleMarker: false,
    rotateMode: false,
});
map.pm.setLang("ru");


map.on('pm:create', function (e) {
  // e.layer is the new layer that was created
  var layer = e.layer;

  var lineLength = turf.length(layer.toGeoJSON(), {units: 'kilometers'});

  // Добавляем подпись к линии
  layer.bindTooltip('Длина: ' + lineLength.toFixed(2) + ' км').openTooltip();



  // Add click event listener to the layer
  layer.on('click', function (event) {
    // Open the Bootstrap modal for editing properties
    $('#propertyModal').modal('show');

    // You can access the clicked layer and its properties here
    var currentColor = layer.options.color || '#ff0000';
    var currentMarkerType = layer.options.icon ? 'circle' : 'square';

    // Populate the form fields with current properties
    $('#color').val(currentColor);
    $('#markerType').val(currentMarkerType);

    // Save a reference to the layer for updating properties
    selectedLayer = layer;
  });
});

var selectedLayer; // Reference to the layer being edited

function updateProperties() {
  // Retrieve values from the form
  var newColor = $('#color').val();
  var newMarkerType = $('#markerType').val();

  // Update the layer properties
  selectedLayer.setStyle({
    color: newColor,
    fillColor: newColor,
    radius: newMarkerType === 'circle' ? 10 : 0, // Adjust radius for circles
  });

  // Close the Bootstrap modal
  $('#propertyModal').modal('hide');
}

document.getElementById('fileInput').addEventListener('change', function (e) {
    var file = e.target.files[0];
    if (file) {
        // Создаем URL из File объекта
        var url = URL.createObjectURL(file);

        // Загрузка KML с помощью leaflet-omnivore
        var kmlLayer = omnivore.kml(url).addTo(map);

        kmlLayer.on('ready', function () {
            // Extract GeoJSON features from the KML layer and add them to geojsonLayer
            var kmlGeoJSON = kmlLayer.toGeoJSON();
            geojsonLayer.addData(kmlGeoJSON);

            // Remove the KML layer
            map.removeLayer(kmlLayer);

            // Revoke the URL after loading
            URL.revokeObjectURL(url);

            // Add click event listener to each feature in the GeoJSON layer
            geojsonLayer.eachLayer(function (layer) {
                layer.on('click', function (event) {
                    // Open the Bootstrap modal for editing properties
                    $('#propertyModal').modal('show');

                    // Access the clicked layer and its properties here
                    var currentColor = layer.options.color || '#ff0000';
                    var currentMarkerType = layer.options.icon ? 'circle' : 'square';

                    // Populate the form fields with current properties
                    $('#color').val(currentColor);
                    $('#markerType').val(currentMarkerType);

                    // Save a reference to the layer for updating properties
                    selectedLayer = layer;
                });
            });
        });
    }
});

var selectedLayer; // Reference to the layer being edited

function updateProperties() {
    // Retrieve values from the form
    var newColor = $('#color').val();
    var newMarkerType = $('#markerType').val();

    // Update the layer properties using Leaflet-Geoman methods
    selectedLayer.pm.enable(); // Enable editing mode

    // Update color
    selectedLayer.setStyle({
        color: newColor,
        fillColor: newColor,
    });

    // Update marker type
    if (newMarkerType === 'circle') {
        selectedLayer.pm.setPathOptions({ shape: 'circle' });
    } else if (newMarkerType === 'square') {
        selectedLayer.pm.setPathOptions({ shape: 'square' });
    }

    selectedLayer.pm.disable(); // Disable editing mode

    // Close the Bootstrap modal
    $('#propertyModal').modal('hide');
}



