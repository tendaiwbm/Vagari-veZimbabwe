from copy import deepcopy
from django.urls import reverse
from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
import distribution.views as v


WARD_POPULATION_URL = reverse("distribution:ward_population")


class TestDistributionViews(TestCase):
    """Test views in the distribution app"""

    def setUp(self):
        self.query_string_parameters = { "admin_level": "ward",
                                         "sex": "total",
                                         "year": 2022,
                                         "apply_filter": "true",
                                         "filter_district": "Mazowe,Mvurwi",
                                         "filter_province": "Matebeleland North,Matebeleland South" }

        self.client = APIClient()
    
    def test_getwardpopulation_http(self):
        """Test get_ward_population exits immediately if HTTP method is not GET"""
        
        expected_response = { "message": "invalid request" }
        
        response = self.client.post(WARD_POPULATION_URL,self.query_string_parameters)
        self.assertEqual(response.json(),expected_response)
            
        response = self.client.put(WARD_POPULATION_URL,self.query_string_parameters)
        self.assertEqual(response.json(),expected_response)
        
        response = self.client.patch(WARD_POPULATION_URL,self.query_string_parameters)
        self.assertEqual(response.json(),expected_response)
        
        response = self.client.options(WARD_POPULATION_URL,self.query_string_parameters)
        self.assertEqual(response.json(),expected_response)

        response = self.client.delete(WARD_POPULATION_URL,self.query_string_parameters)
        self.assertEqual(response.json(),expected_response)
