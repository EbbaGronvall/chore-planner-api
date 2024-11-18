from rest_framework import serializers
from .models import Profile
from households.models import Household
from tasks.models import Task
from tasks.serializers import TaskSerializer


class ProfileSerializer(serializers.ModelSerializer):
    member = serializers.ReadOnlyField(source='member.username')
    is_member = serializers.SerializerMethodField()
    household = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()

    def get_tasks(self, obj):
        tasks = Task.objects.filter(assigned_to=obj)
        return [task.title for task in tasks]

    def get_is_member(self, obj):
        request = self.context['request']
        return request.user == obj.member
    
    def get_household(self, obj):
        if obj.household:
            return obj.household.name
        return "No household"

    class Meta:
        model = Profile
        fields = [
            'id', 'member', 'household', 'role', 'image', 'tasks', 'is_member',
        ]
