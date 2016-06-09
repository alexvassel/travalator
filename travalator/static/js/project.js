/* Project specific Javascript goes here. */

// A $( document ).ready() block.
$( document ).ready(function() {
    initMap();
});

function initMap() {
  // Create a map object and specify the DOM element for display.
  var map = new google.maps.Map(document.getElementById('map_canvas'), {
    center: {lat: -34.397, lng: 150.644},
    scrollwheel: false,
    zoom: 8
  });
}
