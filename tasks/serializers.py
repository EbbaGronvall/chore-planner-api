from rest_framework import serializers
from .models import Task
from profiles.models import Profile

class TaskSerializer(serializers.ModelSerializer):
    task_giver = serializers.ReadOnlyField(source='member.username')
    is_task_giver = serializers.SerializerMethodField()
    assigned_to_username = serializers.ReadOnlyField(source='assigned_to.username')
    

    def get_is_task_giver(self, obj):
        request = self.context['request']
        return request.user == obj.member

    def validate_assigned_to(self, value):
            request = self.context.get('request')
            user_profile = request.user.profile
            if user_profile.role != 'Parent':
                raise serializers.ValidationError('Only parents can assign tasks.')
            
            if user_profile.household != value.household:
                raise serializers.ValidationError('You can only assign tasks to members of the same household as you!')
            return value

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'task_giver', 'is_task_giver',
            'assigned_to', 'assigned_to_username', 'status', 'due_date' 
        ]