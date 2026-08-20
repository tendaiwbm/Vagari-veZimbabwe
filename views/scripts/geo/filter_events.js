// filter state
var FilterState = {
				   "admin-level": "",
				   "granularity": "",
				   "year": "",
				   "sex": "total",
				   "admin-names": new Array(),
				   "zvadzoka": mhinduro
				  };

// validate filters
function validateFilters() {
	if (FilterState["admin-level"] === "") { FilterState["admin-level"] = "ward"; }
	if (FilterState["granularity"] === "") { FilterState["granularity"] = "ward"; }
	if (FilterState["year"] === "") { FilterState["year"] = 2022; }
	if (FilterState["sex"] === "") { FilterState["sex"] = "total"; }
	return true;
}

function tumira(event) {
	if (validateFilters()) {
		if (document.getElementById("admin-names")) { 
			// console.log(document.getElementById("admin-names").style.visibility)
			// if (document.getElementById("admin-names").style.visibility === "visible") {
			// 	document.getElementById("admin-names").style.visibility = "hidden";
			// }
			document.getElementById("admin-names").style.visibility = "hidden";
			document.getElementById("toremovediv").style.height = "23px";
		}
		diridza(FilterState);
	}
}

function adminNamesDropdown(event) {
	if (document.getElementById("admin-names").style.visibility === "hidden") {
		document.getElementById("admin-names").style.visibility = "visible";
		document.getElementById("admin-names").style.height = "200px";
		document.getElementById("toremovediv").style.height = "223px";
	}
	else if (document.getElementById("admin-names").style.visibility === "visible") {
		document.getElementById("admin-names").style.visibility = "hidden";
		document.getElementById("admin-names").style.height = "0px";
		document.getElementById("toremovediv").style.height = "23px";
	}
}

function adminNamesResponseHandler(event,response) {
	var filterContainer = document.getElementById("admin-names-container");
	var names = JSON.parse(response);
	const key = Object.keys(names)[0];
	var namesElement = `
	 					<label id="admin-names-label">${key[0].toUpperCase() + key.slice(1)}</label>
	 					<div id="toremovediv">
 						<div id="admin-names-dummy-searchable">
 							<input id="admin-name-search" type="search" size=21 />
 							<img id="admin-names-dropdown" src="images/dropdown.png" />
 						</div>
 						<div id="admin-names" style="visibility: hidden">
					   `;

	for (i=0;i<names[key].length;i++) {
		namesElement += `<div><input type="checkbox" class="admin-options" name="${names[key][i]}"/><label for="${names[key][i].toLowerCase()}" style="padding-left: 5px">${names[key][i]}</label></div>`;
	}

	namesElement += "</div></div>";
	filterContainer.innerHTML = namesElement;
	document.getElementById("admin-names-label").innerText = key[0].toUpperCase() + key.slice(1);
	document.getElementById("admin-names-dropdown").addEventListener("click",adminNamesDropdown);
	var adminOptions = document.getElementsByClassName("admin-options");
	for (i=0;i<names[key].length;i++) { adminOptions[i].addEventListener("click",updateAdminOptionState); }
}

function updateAdminOptionState(event) {
	if (!(FilterState["admin-names"].includes(event.target.name))) { FilterState["admin-names"].push(event.target.name); }
	else if (FilterState["admin-names"].includes(event.target.name)) {
		FilterState["admin-names"].splice(FilterState["admin-names"].indexOf(event.target.name),1);
	}
	console.log(FilterState);
	
}

// generic update filter state for year & sex
function updateFilterState(event) {
	FilterState[event.srcElement.id] = event.target.value;
	console.log(FilterState);
}

// update admin-level state
function updateAdminLevelState(event) {
	if (FilterState["admin-level"] === event.target.value) { 
		FilterState["admin-level"] = "";
		FilterState["granularity"] = "";
		document.getElementById("grain").getElementsByTagName("option")[3].disabled = false;
    } 
    else {
    	FilterState[event.srcElement.id] = event.target.value;
    	FilterState["granularity"] = "";
    	FilterState["admin-names"] = new Array();
    
		if (event.target.value === "ward") { 
			if (document.getElementById("admin-names")) { 
				document.getElementById("admin-names").remove();
				document.getElementById("admin-names-label").remove(); 
				document.getElementById("admin-names-dummy-searchable").remove();
			}
			FilterState["granularity"] = "ward";
			var grain = document.getElementById("grain");
			grain.value = "ward";
			grain.setAttribute("disabled","true");
		}

		else {
			if (event.target.value != "") {
				document.getElementById("grain").value = "";
				FilterState["granularity"] = event.target.value;
				zvakavanda(event.target.value,adminNamesResponseHandler);
				document.getElementById("grain").removeAttribute("disabled");
				if (event.target.value === "district") { document.getElementById("grain").getElementsByTagName("option")[3].disabled = true; }
				else if (event.target.value === "province") { document.getElementById("grain").getElementsByTagName("option")[3].disabled = false; } 
			}
		}
	}
}

// update granularity state
function updateGrainState(event) {
	FilterState["granularity"] = event.target.value;
}

// Admin Level 
admin = document.getElementById("admin-level");
admin.addEventListener("change",updateAdminLevelState);

// Spatial Granularity
grain = document.getElementById("grain");
grain.addEventListener("change", updateGrainState);

// Year 
t = document.getElementById("year");
t.addEventListener("change", updateFilterState);

// Sex
sex = document.getElementById("sex");
sex.addEventListener("change", updateFilterState); 


// apply filters
dispatcher = document.getElementById("show-label");
dispatcher.addEventListener("click", tumira);
