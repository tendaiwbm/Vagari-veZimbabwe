from django.urls import path
from distribution import views


app_name = "distribution"

urlpatterns = [path('ward/', views.get_ward_population, name="ward_population"),
               path('district/', views.get_district_population, name="district_population"),
               path('province/', views.get_province_population, name="province_distribution"),
               path('names/', views.get_admin_names, name="admin_names")]
