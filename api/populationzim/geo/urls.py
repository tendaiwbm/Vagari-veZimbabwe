from django.urls import path
from .views import Distribution,fetch_admin_names

urlpatterns = [
        path('',Distribution.as_view()),
        path('zvakavanda/',fetch_admin_names),

]

