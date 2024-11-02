from django.shortcuts import get_object_or_404
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Household
from .serializers import HouseholdSerializer
from chore_planner_api.permissions import IsHouseholdMemberOrReadOnly

class HouseholdList(generics.ListAPIView):
    serializer_class = HouseholdSerializer
    queryset = Household.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]
    filterset_fields = [
        'name', 'household_members__username'
    ]
    search_fields = [
        'name', 'household_members__username'
    ]

class HouseholdDetail(generics.RetrieveUpdateAPIView):
    serializer_class = HouseholdSerializer
    queryset = Household.objects.all()
    permission_classes = [IsHouseholdMemberOrReadOnly]
    filter_backends = [
        DjangoFilterBackend
    ]

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Household, slug=slug)