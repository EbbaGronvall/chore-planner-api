from rest_framework import serializers
from .models import Profile
from households.models import Household
from tasks.models import Task
from tasks.serializers import TaskSerializer

class ProfileSerializer(serializers.ModelSerializer):
    member = serializers.ReadOnlyField(source='member.username')
    is_member = serializers.SerializerMethodField()
    household = serializers.PrimaryKeyRelatedField(queryset=Household.objects.all(), many=True)
    household_name = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()

    def get_tasks(self, obj):
        tasks = Task.objects.filter(assigned_to=obj)
        return [task.title for task in tasks]

    def get_is_member(self, obj):
        request = self.context['request']
        return request.user == obj.member

    def get_household_name(self, obj):
        return [household.name for household in obj.household.all()]

    class Meta:
        model = Profile
        fields = [
            'id', 'member', 'household', 'household_name', 'role', 'image', 'tasks', 'is_member',
        ]