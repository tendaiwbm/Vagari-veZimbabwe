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
		if (!(this.category)) {
			throw new Error("Required parameter 'category' missing.");
		};

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

 		return;
 	}
 }