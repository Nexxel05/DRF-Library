from rest_framework import generics

from rest_framework.permissions import IsAuthenticated

from users_service.models import Customer
from users_service.serializers import CustomerSerializer


class CreateCustomerView(generics.CreateAPIView):
    serializer_class = CustomerSerializer


class ManageCustomerView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> Customer:
        return self.request.user
