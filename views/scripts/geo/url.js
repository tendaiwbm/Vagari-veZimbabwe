// 
// 

export class URLBuilder {
	constructor() {

 		// URL query string params
 		this.category = null;
 		this.adminLevel = null;
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

 	updateSex(sex) {
 		this.sex = sex;
 		return this;
 	}

 	updateYear(year) {
 		this.year = year;
 		return this;
 	}

 	updateFilterDistrict(districts) {
 		this.filterDistrict = districts.join(",");
 		return this;
 	}

 	updateFilterProvince(provinces) {
 		this.filterProvince = provinces.join(",");
 		return this;
 	}

 	build() {

		// check required keys first
		if (!(this.adminLevel)) {
			throw new Error("Required parameter 'admin-level' missing.");
		};

		if (!(this.sex)) {
			throw new Error("Required parameter 'sex' missing.");
		}

		if (!(this.year)) {
			throw new Error("Required parameter 'year' missing.");
		}

		let baseUrl = `${window.location.origin}/api/distribution/${this.adminLevel}`;
		let queryString = `admin_level=${this.adminLevel}&sex=${this.sex}&year=${this.year}`;

		if (this.filterDistrict) {
			queryString = `${queryString}&filter_district=${this.filterDistrict}&apply_filter=true`;
		}
		else if (this.filterProvince) {
			queryString = `${queryString}&filter_province=${this.filterProvince}&apply_filter=true`;
		}

 		let url = `${baseUrl}?${queryString}`;

 		return url;
 	}
 }