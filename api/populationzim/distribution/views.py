from django.http import JsonResponse
from django.db.models import Sum
from pandas import DataFrame
from .validators import WardRequestValidator,DistrictRequestValidator
from .models import Ward,District


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
            
            wards = Ward.objects
            districts = District.objects
            if params["apply_filter"] and params["filter_district"]:
                wards = wards.filter(district_name__in=params["filter_district"])
                districts = districts.filter(district_name__in=params["filter_district"])
            
            wards = wards.values("district_name").annotate(district_population=Sum(population_field))
            wards = DataFrame.from_records(wards)
            districts = DataFrame.from_records(districts.values("district_name","geom"))
            districts = districts.merge(wards,how="inner",on="district_name")
            
            response_dict = { "coordinates": [district if len(district[0]) == 1 
                                              else [[district[0][0],[point for point in district[0][1] if point != [0,0]]]]
                                              for district in districts["geom"]],
                              "values": districts["district_population"].to_list(),
                              "names": districts["district_name"].to_list() }
            
            return JsonResponse(response_dict)

    return JsonResponse({"message": "invalid request"})
