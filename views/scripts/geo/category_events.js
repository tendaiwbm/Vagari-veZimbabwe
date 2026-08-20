// category state manager
var CategoryState = {
				     "categorySelected": "",
				     "filterActive": false,	
				    };

function createFilterHTML(category) {
	if (category === "Distribution") {
		return `
				<div id="admin-container">
					<label for="admin-level">Admin Level</label>
					<div>
					<select name="AdminLevels" id="admin-level">
						<option value=""></option>
						<option value="ward">Ward</option>
						<option value="district">District</option>
						<option value="province">Province</option>
					</select>
					</div>
				</div>
				<div id="grain-container">
					<label for="grain">Granularity</label>
					<div>
					<select name="grainValues" id="grain">
						<option value=""></option>
						<option value="ward">Ward</option>
						<option value="district">District</option>
						<option value="province">Province</option>
						</select>
					</div>
				</div>
				<div id="year-container">
					<label for="year">Year</label>
					<div>
					<select id="year" name="yearValues">
						<option value=""></option>
						<option value="2002">2002</option>
						<option value="2012">2012</option>
						<option value="2022">2022</option>
					</select>
					</div>
				</div>
				<div id="sex-container">
					<label for="sex">Sex</label>
					<div>
					<select id="sex" name="sexValues">
						<option value="total"></option>
						<option value="female">F</option>
						<option value="male">M</option>
					</select>
					</div>
				</div>
				<div id="admin-names-container">
				</div>
				<img id="show-label" src="images/ok.png">
				<script type="text/javascript" src="scripts/geo/filter_events.js"></script>`;
	}
}

function toggleFilterContainer(event) {
	if (CategoryState["filterActive"]) {	
		if (CategoryState["categorySelected"] === event.target.innerHTML) {
			CategoryState["categorySelected"] = "";
			CategoryState["filterActive"] = false;
			document.getElementById("filter-container").innerHTML = "";
			return;
		}
	}
	CategoryState["categorySelected"] = event.target.innerHTML;
	CategoryState["filterActive"] = true;
	document.getElementById("filter-container").innerHTML = createFilterHTML(event.target.innerText);
	var filterEvents = document.createElement("script");
	filterEvents.setAttribute("type","text/javascript");
	filterEvents.setAttribute("src","scripts/geo/filter_events.js");
	document.getElementById("filter-container").appendChild(filterEvents);
}

const distro = document.getElementById("distribution");
distro.addEventListener("click",toggleFilterContainer);
const household = document.getElementById("household");
household.addEventListener("click", toggleFilterContainer);





















