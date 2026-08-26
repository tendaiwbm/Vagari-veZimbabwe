from django.contrib import admin
from django.urls import path,include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [path('admin/', admin.site.urls),
               path("api/rondedzero/", SpectacularSwaggerView.as_view(url_name="api-schema"), name="api-docs"),
               path("api/muviri/", SpectacularAPIView.as_view(), name="api-schema"),
               path('api/geo/', include('geo.urls')),
               path("api/distribution/",include("distribution.urls"))]
