from math import log10
from django.http import JsonResponse
from django.db.models import Sum
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from pandas import DataFrame
from .validators import WardRequestValidator,DistrictRequestValidator,ProvinceRequestValidator,AdminNamesRequestValidator
from .models import Ward,District,Province


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_ward_population(request):
    """Handle requests for ward population data"""

    if request.method == "GET":
        ward_request = WardRequestValidator(request.GET)
        
        if ward_request.is_valid():
            params = ward_request.cleaned_data
            population_field = "_".join([params["sex"],"population","density",str(params["year"])])            
            
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
                              "values": [log10(ward[population_field]) 
                                         if ward[population_field] > 0
                                         else 0
                                         for ward in data] }

            return JsonResponse(response_dict)

    return JsonResponse({"message": "invalid request"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_district_population(request):
    """Handle requests for district population data"""

    if request.method == "GET":
        district_request = DistrictRequestValidator(request.GET)
        
        if district_request.is_valid():
            params = district_request.cleaned_data
            population_field = "_".join([params["sex"],"population","density",str(params["year"])])            
            
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
                              "values": list(map(log10,districts["district_population"].to_list())),
                              "names": districts["district_name"].to_list() }
            
            return JsonResponse(response_dict)

    return JsonResponse({"message": "invalid request"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_province_population(request):
    """Handle requests for province population data"""

    if request.method == "GET":
        province_request = ProvinceRequestValidator(request.GET)
        
        if province_request.is_valid():
            params = province_request.cleaned_data
            population_field = "_".join([params["sex"],"population","density",str(params["year"])])            
            
            wards = Ward.objects
            provinces = Province.objects
            if params["apply_filter"] and params["filter_province"]:
                wards = wards.filter(province_name__in=params["filter_province"])
                provinces = provinces.filter(province_name__in=params["filter_province"])
            
            wards = wards.values("province_name").annotate(province_population=Sum(population_field))
            wards = DataFrame.from_records(wards)
            provinces = DataFrame.from_records(provinces.values("province_name","geom"))
            provinces = provinces.merge(wards,how="inner",on="province_name")
           
            response_dict = { "coordinates": [province if len(province[0]) == 1 
                                              else [[province[0][0],[point for point in province[0][1] if point != [0,0]]]]
                                              for province in provinces["geom"]],
                              "values": list(map(log10,provinces["province_population"].to_list())),
                              "names": provinces["province_name"].to_list() }

            return JsonResponse(response_dict)
        
    return JsonResponse({"message": "invalid request"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_admin_names(request):
    """Provide a list of all district/province names"""

    if request.method == "GET":
        names_request = AdminNamesRequestValidator(request.GET)

        if names_request.is_valid():
            params = names_request.cleaned_data
            names_column = "_".join([params["admin_level"],"name"])

            if params["admin_level"] == "district":
                admin_names_model = District
            elif params["admin_level"] == "province":
                admin_names_model = Province

            names = admin_names_model.objects.values(names_column)

            return JsonResponse({ "names": [name[key] for name in names for key in name] })

    return JsonResponse({ "message": "invalid" })
    
