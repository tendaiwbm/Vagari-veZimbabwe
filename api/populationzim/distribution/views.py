from django.http import JsonResponse
from .validators import WardRequestValidator,DistrictRequestValidator
from .models import Ward


def get_ward_population(request):
    """Handle requests for ward population data"""

    if request.method == "GET":
        ward_request = WardRequestValidator(request.GET)
        
        if ward_request.is_valid():
            params = ward_request.cleaned_data
            population_field = "_".join([params["sex"],"population",str(params["year"])])            
            
            data = Ward.objects
            if params["apply_filter"]:
                if params["filter_district"]:
                    data = data.filter(district_name__in=params["filter_district"])
                elif params["filter_province"]:
                    data = data.filter(province_name__in=params["filter_province"])
                 
            data = data.values(population_field,"geom")
            
            response_dict = { "coordinates": [ward["geom"] if len(ward["geom"][0]) == 1 
                                              else [[ward["geom"][0][0],[point for point in ward["geom"][0][1] if point != [0,0]]]]
                                              for ward in data],
                              "values": [ward[population_field] for ward in data] }

            return JsonResponse(response_dict)

    return JsonResponse({"message": "invalid request"})

def get_district_population(request):
    """Handle requests for district population data"""

    if request.method == "GET":
        district_request = DistrictRequestValidator(request.GET)
        
        if district_request.is_valid():
            params = district_request.cleaned_data
            population_field = "_".join([params["sex"],"population",str(params["year"])])            
            

            
            return JsonResponse({"message": "valid"})

    return JsonResponse({"message": "invalid request"})

