from django.urls import path
from distribution import views


urlpatterns = [path('ward/', views.get_ward_population),
               path('district/', views.get_district_population),
               path('province/', views.get_province_population),
               path('names/', views.get_admin_names)]
