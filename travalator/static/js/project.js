/* Project specific Javascript goes here. */

// A $( document ).ready() block.
$( document ).ready(function() {
    initMap();
});

function initMap() {
    // Create a map object and specify the DOM element for display.
    var mapElement = document.getElementById('map_canvas');
    var centerPoint = new google.maps.LatLng($(mapElement).data('long'), $(mapElement).data('lat'));
    var map = new google.maps.Map(mapElement, {
    center: centerPoint,
    scrollwheel: true,
    zoom: 8
  });
}
