function includeHTMLPHPFile(filePath, placeHolder) {
    $(document).ready(function() {
        $.ajax({
            type: 'get',
            url: '/URLToTriggerGetRequestHandler',
            cache: false,
            async: 'asynchronous',
            dataType: 'json',
            beforeSend: function() {
                $('#' + placeHolder).html('<div class="progress"><div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%">Procesando</div></div>');
            },
            success: function(data) {
                lat = -1.6448868;
                long = -79.1440891;
                cordEC = data
                $("#" + placeHolder).load(filePath);
            },
            error: function(request, status, error) {
                $('#Espera').html('Datos cargados');
                console.log("Error: " + error)
            }
        });
    });
}

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(myMap);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function myMap() {
    var Ecuador = new google.maps.LatLng(lat, long);

    map = new google.maps.Map(document.getElementById('googleMap'), {
        center: Ecuador,
        zoom: 7
    });
    var heatmapData = [];
    var heatmapData2 = [];
    for (var i = 0; i < Object.keys(cordEC['sentiment']).length; i++) {
        var latCord = cordEC['coords']['coordenadas' + i.toString()].lat;
        var longCotd = cordEC['coords']['coordenadas' + i.toString()].long;
        var obj = new google.maps.LatLng(latCord, longCotd);
        if (cordEC['sentiment']['sentiment' + i.toString()].sent <= 0) {
            heatmapData.push(obj);
        } else {
            heatmapData2.push(obj)
        }
    }

    var heatmap = new google.maps.visualization.HeatmapLayer({
        data: heatmapData,
        radius: 15,
        maxIntensity: 10
    });
    var gradient = [
        'rgba(0, 255, 255, 0)',
        'rgba(0, 255, 255, 1)',
        'rgba(0, 191, 255, 1)',
        'rgba(0, 127, 255, 1)',
        'rgba(0, 63, 255, 1)',
        'rgba(0, 0, 255, 1)',
        'rgba(0, 0, 223, 1)',
        'rgba(0, 0, 191, 1)',
        'rgba(0, 0, 159, 1)',
        'rgba(0, 0, 127, 1)',
        'rgba(63, 0, 91, 1)',
        'rgba(127, 0, 63, 1)',
        'rgba(191, 0, 31, 1)',
        'rgba(255, 0, 0, 1)'
    ]
    heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
    heatmap.setMap(map);
    var heatmap2 = new google.maps.visualization.HeatmapLayer({
        data: heatmapData2,
        radius: 10,
        maxIntensity: 10
    });
    heatmap2.setMap(map);

}