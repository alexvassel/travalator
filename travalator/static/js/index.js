/**
 * Created by vasilev on 10.06.16.
 */

$( document ).ready(function() {
    var mapElement = document.getElementById('map_canvas');

    if (mapElement !== null) {
        var map = initMap(mapElement);

        $.ajax({
            url: $(mapElement).data('points')
        }).done(function (response) {
            if (response.error !== undefined) {
                console.log(response.message);
                return
            }
            setMarkers(response.data.points, map);
            setLines(response.data.points, map);
        });
    }
});

function initMap(mapElement) {
    var centerPoint = {lat: $(mapElement).data('lat'), lng: $(mapElement).data('lng')};
    return new google.maps.Map(mapElement, {
        center: centerPoint,
        scrollwheel: true,
        zoom: 8
    });
}

function setMarkers(points, map) {
    $.each(points, function(_, point) {
        var marker = new google.maps.Marker({
            position: {lat: point.location[1], lng: point.location[0]},
            title: point.name,
            animation: google.maps.Animation.DROP
        });
        setMarkerInfo(point, marker, map);
        marker.setMap(map);
    });
}

function setMarkerInfo(point, marker, map) {
    var infowindow = new google.maps.InfoWindow({content: point.description});
    marker.addListener('click', function() {
        infowindow.open(map, marker);
    });
}

function setLines(points, map) {
    var routePoints = [];
    var lineSymbol = {path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW};

    $.each(points, function(_, point) {
        routePoints.push({lat: point.location[1], lng: point.location[0]});
        var flightPath = new google.maps.Polyline({
            path: routePoints,
            geodesic: true,
            strokeColor: '#FF0000',
            strokeOpacity: 1.0,
            strokeWeight: 2,
            icons: [{
              icon: lineSymbol,
              offset: '100%'
            }]});
        flightPath.setMap(map);
    });
}
