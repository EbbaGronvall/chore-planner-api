from rest_framework import serializers
from .models import Profile
from households.models import Household
from tasks.models import Task
from tasks.serializers import TaskSerializer


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model, providing additional computed fields.
    """
    member = serializers.ReadOnlyField(source='member.username')
    is_member = serializers.SerializerMethodField()
    household_name = serializers.SerializerMethodField()
    household_slug = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()

    def get_tasks(self, obj):
        """
        Retrieves tasks assigned to the profile.
        """
        tasks = Task.objects.filter(assigned_to=obj)
        if not tasks.exists():
            return []
        return [task.title for task in tasks]

    def get_is_member(self, obj):
        """
        Checks if the request user matches the profile's user.
        """
        request = self.context['request']
        return request.user == obj.member

    def get_household_name(self, obj):
        """
        Retrieves the name of the household associated with the profile.
        """
        if obj.household:
            return obj.household.name
        return "No household"

    def get_household_slug(self, obj):
        """
        Retrieves the slug of the household associated with the profile.
        """
        if obj.household:
            return obj.household.slug
        return None

    def validate(self, data):
        """
        Validates and processes household_slug during updates.
        """
        request = self.context['request']
        if request.method == 'PUT' and 'household_slug' in request.data:
            household_slug = request.data.get('household_slug')
            if household_slug:
                try:
                    household = Household.objects.get(slug=household_slug)
                    data['household'] = household
                except Household.DoesNotExist:
                    raise ValidationError({
                                'household_slug':
                                'Household with this slug does not exist.'
                                })
        return data

    class Meta:
        model = Profile
        fields = [
            'id', 'member', 'household_name', 'household_slug', 'role',
            'image', 'tasks', 'is_member',
        ]
