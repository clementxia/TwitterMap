
// Create the XHR object.

function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 0, lng: 0},
    zoom: 3,
    styles: [{
      featureType: 'poi',
      stylers: [{ visibility: 'on' }]  // Turn off points of interest.
    }, {
      featureType: 'transit.station',
      stylers: [{ visibility: 'on' }]  // Turn off bus stations, train stations, etc.
    }],
    disableDoubleClickZoom: false
  });
 
}

function searchmap(){
	var quer = document.getElementById('search').value;
	var url = "http://my-app.zi6pvgqmcn.us-west-2.elasticbeanstalk.com/search";

  var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 0, lng: 0},
    zoom: 3,
    styles: [{
      featureType: 'poi',
      stylers: [{ visibility: 'on' }]  // Turn off points of interest.
    }, {
      featureType: 'transit.station',
      stylers: [{ visibility: 'on' }]  // Turn off bus stations, train stations, etc.
    }],
    disableDoubleClickZoom: false
  });


	var xmlhttp = new XMLHttpRequest();
	xmlhttp.open("GET", url, true);
  xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
      var obj = JSON.parse(xmlhttp.responseText);
      alert(obj.length);
      for (i = 0; i < obj.length; i++) {
        var lo = {lat: obj[i]['lat'], lng: obj[i]['lon']};
        var marker = new google.maps.Marker({
          position: lo,
          map: map
        });
      }
    }
  }
  xmlhttp.send(); 
}


