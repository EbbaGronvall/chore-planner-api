from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    task_giver_username = serializers.ReadOnlyField(
                                        source='task_giver.member.username'
                                        )
    is_task_giver = serializers.SerializerMethodField()
    assigned_to_username = serializers.ReadOnlyField(
                                        source='assigned_to.member.username'
                                        )

    def get_is_task_giver(self, obj):
        """
        Determines if the request user is the task giver.
        """
        request = self.context['request']
        return request.user == obj.task_giver.member

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'task_giver_username',
            'is_task_giver', 'assigned_to', 'assigned_to_username', 'status',
            'due_date'
        ]
