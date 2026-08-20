// 
// 

export class URLBuilder {
	constructor() {

 		// URL query string params
 		this.category = null;
 		this.adminLevel = null;
 		this.grain = null;
 		this.sex = null;
 		this.year = null;
 		this.filterDistrict = null;
 		this.filterProvince = null;
 	}

 	updateCategory(category) {
 		this.category = category;
 		return this;
 	}

 	updateAdminLevel(adminLevel) {
 		this.adminLevel = adminLevel;
 		return this;
 	}

 	updateGranularity(grain) {
 		this.grain = grain;
 		return this;
 	}

 	updateSex(sex) {
 		this.sex = sex;
 		return this;
 	}

 	updateYear(year) {
 		this.year = year;
 		return this;
 	}

 	updateFilterDistrict(districts) {
 		this.filterDistricts = districts.join(",");
 		return this;
 	}

 	updateFilterProvince(provinces) {
 		this.filterProvinces = provinces.join(",");
 		return this;
 	}

 	build() {

		// check required keys first
		if (!(this.adminLevel)) {
			throw new Error("Required parameter 'admin-level' missing.");
		};
			
		if (!(this.grain)) {
			throw new Error("Required parameter 'granularity' missing.");
		}

		if (!(this.sex)) {
			throw new Error("Required parameter 'sex' missing.");
		}

		if (!(this.year)) {
			throw new Error("Required parameter 'year' missing.");
		}

		let baseUrl = `${window.location.origin}/api/distribution/${this.adminLevel}`;
		let queryString = `admin_level=${this.adminLevel}&grain=${this.grain}&sex=${this.sex}&year=${this.year}`;

		if (this.filterDistrct) {
			queryString = `${queryString}&filter_district=${this.filterDistrict}`;
		}
		else if (this.filterProvince) {
			queryString = `${queryString}&filter_province=${this.filterProvince}`;
		}

 		let url = `${baseUrl}?${queryString}`;

 		return url;
 	}
 }