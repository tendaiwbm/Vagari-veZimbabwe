from copy import deepcopy
from django.test import TestCase
from django.core.exceptions import ValidationError
import distribution.validators as v


class FormValidationTests(TestCase):
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
 
