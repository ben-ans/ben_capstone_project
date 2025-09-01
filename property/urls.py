from django.urls import path
from .views import PropertyListView, PropertyCreateView

urlpatterns = [
    path('', PropertyListView.as_view(), name='property-list'),
    path('create/', PropertyCreateView.as_view(), name='property-create'),
]
