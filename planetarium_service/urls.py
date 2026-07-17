from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/planetarium/",
        include(
            "planetarium_app.urls",
            namespace="planetarium_app"
        )
    ),
    path("api/v1/user/", include("user.urls", namespace="user")),
]
