from rest_framework import serializers
from .models import Profile
from households.models import Household
from tasks.models import Task
from tasks.serializers import TaskSerializer


class ProfileSerializer(serializers.ModelSerializer):
    member = serializers.ReadOnlyField(source='member.username')
    is_member = serializers.SerializerMethodField()
    household_name = serializers.SerializerMethodField()
    household_slug = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()

    def get_tasks(self, obj):
        tasks = Task.objects.filter(assigned_to=obj)
        if not tasks.exists():
            return []
        return [task.title for task in tasks]

    def get_is_member(self, obj):
        request = self.context['request']
        return request.user == obj.member
    
    def get_household_name(self, obj):
        if obj.household:
            return obj.household.name
        return "No household"

    def get_household_slug(self, obj):
        if obj.household:
            return obj.household.slug
        return None
    

    class Meta:
        model = Profile
        fields = [
            'id', 'member', 'household_name', 'household_slug', 'role', 'image', 'tasks', 'is_member',
        ]
