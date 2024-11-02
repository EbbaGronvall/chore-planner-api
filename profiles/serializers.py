from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    member = serializers.ReadOnlyField(source='member.username')
    is_member = serializers.SerializerMethodField()

    def get_is_member(self, obj):
        request = self.context['request']
        return request.user == obj.member


    class Meta:
        model = Profile
        fields = [
            'id', 'member', 'role', 'image', 'is_member',
        ]