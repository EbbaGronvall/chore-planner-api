from rest_framework import serializers
from .models import Household
from profiles.models import Profile


class HouseholdSerializer(serializers.ModelSerializer):
    household_members = serializers.SerializerMethodField()

    def get_household_members(self, obj):
        """
        Retrieves the usernames of the household members.
        """
        return [profile.member.username for profile in obj.members.all()]

    class Meta:
        model = Household
        fields = [
            'id', 'name', 'slug', 'household_members',
        ]
