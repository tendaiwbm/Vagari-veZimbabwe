from geo.data_validation import distro_validator,admin_validator
from geo.utils import query_munyayi,prepare_admin_names
from django.views import View
from django.http import JsonResponse
from math import log10

class Distribution(View):
    category = "Distribution"
    
    def prepare_distribution(self,query):
        queryResult = query_munyayi(query)
        geom = (pair[1] for pair in queryResult)
        RESPONSE = {
                    "coordinates": [polygon if len(polygon[0]) == 1 else [[polygon[0][0],[point for point in polygon[0][1] if point != [0,0]]]] for polygon in geom],
                    "admin-level": "district",
                    "grain": "ward",
                    "values": [log10(pair[0]) if pair[0] > 0 else pair[0] for pair in queryResult],
                   }
        return RESPONSE

    def get(self,request):
        print(self)
        if distro_validator(request.GET):
            
            if request.GET['grain'] == "ward":
                query = f"""select {request.GET['sex']}_population_density_{request.GET['year']},geom from prelim.{request.GET['grain']}"""
                if "admin-names" in request.GET:
                    query = " ".join([query,f"""where {request.GET['admin']}_name in""","""""".join(["(",",".join([f"'{name}'" for name in request.GET["admin-names"].split(";")]),")"])])
            
            elif request.GET['grain'] in ["district","province"]:
                query = f"""
                            SELECT sum(b.{request.GET['sex']}_population_density_{request.GET['year']}),geom
                            FROM prelim.{request.GET['grain']} AS a
                            JOIN 
                         """
                subQuery = f"""(SELECT {request.GET['sex']}_population_density_{request.GET['year']},{request.GET['admin']}_name
                               FROM prelim.ward""" 
                if "admin-names" in request.GET:
                    subQuery = " ".join([subQuery,f"""WHERE {request.GET['admin']}_name in""","""""".join(["(",",".join([f"'{name}'" for name in request.GET["admin-names"].split(";")]),")"])])
                
                query = """""".join([query,subQuery, f""") as b ON a.{request.GET['admin']}_name = b.{request.GET['admin']}_name GROUP BY a.geom"""])
            return JsonResponse(self.prepare_distribution(query))

@prepare_admin_names
def fetch_admin_names(request):
    if admin_validator(request.GET):
        query = f"""SELECT {request.GET['admin']}_name FROM prelim.{request.GET['admin']}"""
        return query_munyayi(query)
