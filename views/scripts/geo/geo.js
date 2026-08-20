(function displayFilterWindow(event) {
	var projectName = "populationZim";
	console.log("Starting: " + projectName + " --> geo.");
})();

var map = L.map('map', {
						 crs: L.CRS.EPSG4326,
						 layers: [],
						 center: [-17.817452,31.052431],
						 zoom: 12.5,	
						}
				);

map.attributionControl.setPrefix("");


function colour(feature) {
	return feature > 3.25 ? "#a8281eff" : 
		   feature > 2.00 ? "#d83020ff" :
		   feature > 1.25 ? "#f07062ff" :
		   					"#f89b91ff" ;
};	

function geometryResponseHandler(response) {
	for (i=0;i<response["coordinates"].length;i++) {
		L.polygon(response["coordinates"][i],{
											  color: "black",
											  weight: 1.5,
											  fillColor: colour(response["values"][i]), 
											  fillOpacity: 1,
											  attributes: {
											  				"pop": response["values"][i]
											  			  }
								             }
		).addTo(map);
	}
	map.attributionControl.addAttribution("ZIMSTAT  |  Leaflet  |  HDX  |  ESRI")
	map.zoomControl.setPosition("topright");
	document.getElementById("filter-container").style.opacity = "60%";
}
