from rest_framework import serializers
from .models import Household


class HouseholdSerializer(serializers.ModelSerializer):
    household_members = serializers.SerializerMethodField()

    def get_household_members(self, obj):
        return [profile.username for profile in obj.household_members.all()]

    class Meta:
        model = Household
        fields = [
            'id', 'name', 'slug', 'household_members',
        ]