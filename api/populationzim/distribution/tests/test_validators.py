from copy import deepcopy
from django.test import TestCase
from django.core.exceptions import ValidationError
import distribution.validators as v


class BaseValidatorTests(TestCase):
    """Tests for validation forms"""
    
    def setUp(self):
        self.query_string_parameters = { "admin_level": "ward",
                                         "sex": "total",
                                         "year": 2022,
                                         "apply_filter": "true",
                                         "filter_district": "Mazowe,Mvurwi",
                                         "filter_province": "Matebeleland North,Matebeleland South" }

    def test_admin_level_missing(self):
        """Test validation raises error when admin_level not in query string"""

        params = deepcopy(self.query_string_parameters)
        params_to_drop = ("filter_district","filter_province","apply_filter","admin_level")
        for param in params_to_drop:
            params.pop(param)
        
        validator = v.BaseDistributionRequestValidator(params)
        with self.assertRaises(AssertionError):
            self.assertTrue(validator.is_valid())
   
    def test_sex_missing(self):
        """Test validation raises error when sex not in query string"""

        params = deepcopy(self.query_string_parameters)
        params_to_drop = ("filter_district","filter_province","apply_filter","sex")
        for param in params_to_drop:
            params.pop(param)
        
        validator = v.BaseDistributionRequestValidator(params)
        self.assertTrue(validator.is_valid())
    
    def test_year_missing(self):
        """Test validation raises error when year not in query string"""

        params = deepcopy(self.query_string_parameters)
        params_to_drop = ("filter_district","filter_province","apply_filter","year")
        for param in params_to_drop:
            params.pop(param)
        
        validator = v.BaseDistributionRequestValidator(params)
        with self.assertRaises(AssertionError):
            self.assertTrue(validator.is_valid())

    def test_applyfilter_no_values(self):
        """Test validation raises error when no values for filter_district or filter_province provided"""

        params = deepcopy(self.query_string_parameters)
        params_to_update = ("filter_district","filter_province")
        for param in params_to_update:
            params[param] = ""
        
        validator = v.BaseDistributionRequestValidator(params)
        validator.cleaned_data = params

        with self.assertRaises(ValidationError):
            validator.clean()

    def test_applyfilter_unaccompanied(self):
        """Test validation behaviour when apply_filter not paired with filter_district or filter_province"""

        params = deepcopy(self.query_string_parameters)
        params_to_drop = ("filter_district","filter_province")
        for param in params_to_drop:
            params.pop(param)
        
        validator = v.BaseDistributionRequestValidator(params)
        validator.cleaned_data = params

        with self.assertRaises(KeyError):
            validator.clean()

    def test_filterdistrict_aslist(self):
        """Test districts parsed from query string returned as list of length >= 1"""

        params = deepcopy(self.query_string_parameters)
        params_to_drop = ("filter_province",)
        for param in params_to_drop:
            params.pop(param)
        
        validator = v.BaseDistributionRequestValidator(params)
        self.assertTrue(validator.is_valid())

        filter_by_districts = validator.cleaned_data["filter_district"]
        self.assertTrue(isinstance(filter_by_districts,list))
        self.assertTrue(len(filter_by_districts) >= 1)

    def test_filterprovince_aslist(self):
        """Test provinces parsed from query string returned as list of length >= 1"""

        params = deepcopy(self.query_string_parameters)
        params_to_drop = ("filter_district",)
        for param in params_to_drop:
            params.pop(param)
        
        validator = v.BaseDistributionRequestValidator(params)
        self.assertTrue(validator.is_valid())

        filter_by_provinces = validator.cleaned_data["filter_province"]
        self.assertTrue(isinstance(filter_by_provinces,list))
        self.assertTrue(len(filter_by_provinces) >= 1)


class AdminValidatorTests(TestCase):
    """Tests for Ward, District & Province request validators"""

    def setUp(self):
        self.query_string_parameters = { "admin_level": "ward",
                                         "sex": "total",
                                         "year": 2022,
                                         "apply_filter": "true",
                                         "filter_district": "Mazowe,Mvurwi",
                                         "filter_province": "Matebeleland North,Matebeleland South" }

    def test_ward_admin_level(self):
        """Test other admin_level value triggers validation failure for WardRequestValidator"""

        params = deepcopy(self.query_string_parameters)
        params["admin_level"] = "unknown"

        validator = v.WardRequestValidator(params)
        with self.assertRaises(AssertionError):
            self.assertTrue(validator.is_valid())
    
    def test_district_admin_level(self):
        """Test other admin_level value triggers validation failure for DistrictRequestValidator"""

        params = deepcopy(self.query_string_parameters)
        params["admin_level"] = "unknown"

        validator = v.DistrictRequestValidator(params)
        with self.assertRaises(AssertionError):
            self.assertTrue(validator.is_valid())

    def test_province_admin_level(self):
        """Test other admin_level value triggers validation failure for ProvinceRequestValidator"""

        params = deepcopy(self.query_string_parameters)
        params["admin_level"] = "unknown"

        validator = v.ProvinceRequestValidator(params)
        with self.assertRaises(AssertionError):
            self.assertTrue(validator.is_valid())
