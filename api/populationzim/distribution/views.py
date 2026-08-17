from django.http import JsonResponse
from .validators import WardRequestValidator


def get_ward_population(request):
    
    if request.method == "GET":
        ward_request = WardRequestValidator(request.GET)
        
        if ward_request.is_valid():
            return JsonResponse({"key": "valid"})

    return JsonResponse({"key": "invalid"})
