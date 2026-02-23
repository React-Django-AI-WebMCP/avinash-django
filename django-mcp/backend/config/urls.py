from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/time-tracking/", include("time_tracker.urls")),
    path("", include("core.urls")),
]
