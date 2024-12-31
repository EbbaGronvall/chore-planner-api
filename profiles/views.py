from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Profile
from .serializers import ProfileSerializer
from chore_planner_api.permissions import IsMemberOrReadOnly


class ProfileList(generics.ListAPIView):
    """
    API view for listing profiles.
    """
    serializer_class = ProfileSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]
    filterset_fields = ['role', 'household']
    search_fields = ['member__username']

    def get_queryset(self):
        """
        Retrieves the queryset of profiles based on the authenticated
        user's household.
        """
        user = self.request.user
        if not user.is_authenticated:
            return Profile.objects.none()
        return Profile.objects.filter(household=user.profile.household)


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating a specific profile.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsMemberOrReadOnly]
    queryset = Profile.objects.all()
