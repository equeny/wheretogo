 

    function bound(value, opt_min, opt_max) {
      if (opt_min != null) value = Math.max(value, opt_min);
      if (opt_max != null) value = Math.min(value, opt_max);
      return value;
    }

    function degreesToRadians(deg) {
      return deg * (Math.PI / 180);
    }

    function radiansToDegrees(rad) {
      return rad / (Math.PI / 180);
    }

    function MercatorProjection() {
      this.pixelOrigin_ = new google.maps.Point(TILE_SIZE / 2,
          TILE_SIZE / 2);
      this.pixelsPerLonDegree_ = TILE_SIZE / 360;
      this.pixelsPerLonRadian_ = TILE_SIZE / (2 * Math.PI);
    }

    MercatorProjection.prototype.fromLatLngToPoint = function(latLng,
        opt_point) {
      var me = this;
      var point = opt_point || new google.maps.Point(0, 0);
      var origin = me.pixelOrigin_;

      point.x = origin.x + latLng.lng() * me.pixelsPerLonDegree_;

      // NOTE(appleton): Truncating to 0.9999 effectively limits latitude to
      // 89.189.  This is about a third of a tile past the edge of the world
      // tile.
      var siny = bound(Math.sin(degreesToRadians(latLng.lat())), -0.9999,
          0.9999);
      point.y = origin.y + 0.5 * Math.log((1 + siny) / (1 - siny)) *
          -me.pixelsPerLonRadian_;
      return point;
    };

    MercatorProjection.prototype.fromPointToLatLng = function(point) {
      var me = this;
      var origin = me.pixelOrigin_;
      var lng = (point.x - origin.x) / me.pixelsPerLonDegree_;
      var latRadians = (point.y - origin.y) / -me.pixelsPerLonRadian_;
      var lat = radiansToDegrees(2 * Math.atan(Math.exp(latRadians)) -
          Math.PI / 2);
      return new google.maps.LatLng(lat, lng);
    };


  var onloading = function() {
    var mapOptions = {
      zoom: 12,
      center: new google.maps.LatLng(50.45000001,30.50000001),
      mapTypeId: google.maps.MapTypeId.TERRAIN
    };

    var map = new google.maps.Map(document.getElementById("map_canvas"),
        mapOptions); 
    
	var circ = undefined;
	var point = undefined;
	var radius = 2000;
    jQuery('#m').on('click', function(event) {
        radius -= (radius >= 1000)?500:0;
        circ.setRadius(radius);
	});      
    jQuery('#p').on('click', function(event) {
        radius += (radius <= 10000)?500:0;    	 
    	circ.setRadius(radius);
    }); 
 
    google.maps.event.addListener(map, 'click', function(event) {
    	 
    	var populationOptions = {
    	        strokeColor: "#FF0000",
    	        strokeOpacity: 0.8,
    	        strokeWeight: 2,
    	        fillColor: "#FF0000",
    	        fillOpacity: 0.35,
    	        map: map,
    	        center: event.latLng,
    	        radius: radius
    	      };
    	circ = circ || new google.maps.Circle(populationOptions);     
    	point = point || new google.maps.Marker({
            position: event.latLng,
            map: map,
            title: 'Your event place range'
          });
     });
    
  }

  $(document).ready(onloading);