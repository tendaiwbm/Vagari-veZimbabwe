from geo.worker import request_handler
from django.http import JsonResponse
import math


def prepare_admin_names(decoratee):
    def wrapper(query):
        return JsonResponse({query.GET["admin"]:[admin[0] for admin in decoratee(query)]})
    return wrapper

@request_handler
def query_munyayi(query):
    return query


def new_function():
    print("testing git checkout file")
