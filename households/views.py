from django.shortcuts import get_object_or_404
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Household
from .serializers import HouseholdSerializer
from chore_planner_api.permissions import IsHouseholdMemberOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from profiles.models import Profile


class HouseholdList(generics.ListCreateAPIView):
    serializer_class = HouseholdSerializer
    queryset = Household.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]
    filterset_fields = [
        'name'
    ]
    search_fields = [
        'name', 'members__member__username'
    ]
    def perform_create(self, serializer):
        household = serializer.save()
        user = self.request.user
        user.profile.household = household
        user.profile.save()

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
