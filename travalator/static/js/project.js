/* Project specific Javascript goes here. */

// A $( document ).ready() block.
$( document ).ready(function() {
    var mapElement = document.getElementById('map_canvas');
    var map = initMap(mapElement);

    $.ajax({
        url: '/route/' + $(mapElement).data('route') + '/points/'
    }).done(function(response) {
        if (response.error !== undefined) {console.log(response.message)}
        setMarkers(response.data.points, map);
    });
});

function initMap(mapElement) {
    var centerPoint = {lat: $(mapElement).data('lat'), lng: $(mapElement).data('lng')};
    return new google.maps.Map(mapElement, {
    center: centerPoint,
    scrollwheel: true,
    zoom: 6
  });
}

function setMarkers(points, map) {
    $.each(points, function(_, point) {

        var marker = new google.maps.Marker({
            position: {lat: point.location[1], lng: point.location[0]},
            title: point.name,
            animation: google.maps.Animation.DROP,
        });
        setMarkerInfo(point, marker, map);
        marker.setMap(map);
    });
}

function setMarkerInfo(point, marker, map) {
    var infowindow = new google.maps.InfoWindow({
            content: point.description
    });
    marker.addListener('click', function() {
        infowindow.open(map, marker);
    });
}
