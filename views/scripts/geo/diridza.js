import { URLBuilder } from "./url.js"

var API_GEO_STUB = "api/geo";

function munyayi(mahobho,responseHandler) {
	var mutumwa = new XMLHttpRequest();
	mutumwa.onreadystatechange = function(event) {
	 	if (mutumwa.readyState === 4 && mutumwa.status === 200) {
	 		responseHandler(event,mutumwa.response);
	 	}
	}
	mutumwa.open("GET",mahobho,true);
	mutumwa.send();
}

// penengura mhinduro, gadzirisa map
export function mhinduro(event,mutumwa) {
	console.log(event);
	const map = document.getElementById("map");
	CategoryState["filterActive"] = false;
	document.getElementById("map").style.visibility = "visible";
	geometryResponseHandler(JSON.parse(mutumwa));
	//map.innerText = JSON.stringify(JSON.parse(mutumwa),undefined,2);
}


// tumira, penengura mhinduro, gadzirisa map
export function diridza(params) {
	var builder = new URLBuilder().
					  updateCategory(CategoryState["categorySelected"].toLowerCase()).
					  updateAdminLevel(params["admin-level"]).
					  updateGranularity(params["granularity"]).
					  updateSex(params["sex"]).
					  updateYear(params["year"]);

	if (params["admin-names"]) {
		if (params["admin-level"] === "district") {
			builder.updateFilterDistrict(params["admin-names"]);
		}
		else if (params["admin-level"] === "province") {
			builder.updateFilterProvince(params["admin-names"]);
		}
	}
	
	let url = builder.build()

	munyayi(url,params["zvadzoka"]);

	return;
}

function zvakavanda(level,responseHandler) {
	var mahobho = `${BASE}${API_GEO_STUB}/zvakavanda?admin=${level}`;
	console.log("Meta URL  >>  " + mahobho);
	munyayi(mahobho,responseHandler);
}