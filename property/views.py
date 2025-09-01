from rest_framework import generics, permissions
from .models import Property
from .serializers import PropertySerializer

class PropertyListView(generics.ListAPIView):
    queryset = Property.objects.all().order_by('-created_at')
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]  # anyone can view

class PropertyCreateView(generics.CreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # Only allow landlords to create properties
        if self.request.user.role != 'landlord':
            raise PermissionError("Only landlords can upload properties.")
        serializer.save(landlord=self.request.user)
