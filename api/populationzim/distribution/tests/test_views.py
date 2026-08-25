from copy import deepcopy
from django.urls import reverse
from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
import distribution.views as v


WARD_POPULATION_URL = reverse("distribution:ward_population")
DISTRICT_POPULATION_URL = reverse("distribution:district_population")
PROVINCE_POPULATION_URL = reverse("distribution:province_population")
ADMIN_NAMES_URL = reverse("distribution:admin_names")


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
    
    def test_distribution_get_only(self):
        """Test requests to distribution endpoints return error message when HTTP method is not GET"""

        urls = [WARD_POPULATION_URL,
                DISTRICT_POPULATION_URL,
                PROVINCE_POPULATION_URL,
                ADMIN_NAMES_URL]

        for url in urls:
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
