from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users_service.views import CreateCustomerView, ManageCustomerView

urlpatterns = [
    path("", CreateCustomerView.as_view(), name="create"),
    path("me", ManageCustomerView.as_view(), name="manage"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

app_name = "users_service"
