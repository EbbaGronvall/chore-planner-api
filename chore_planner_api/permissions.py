from rest_framework import permissions


class IsMemberOrReadOnly(permissions.BasePermission):
    """
    Makes sure that only the owner of the profile can edit it
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.member == request.user


class IsHouseholdMemberOrReadOnly(permissions.BasePermission):
    """
    Makes sure that only household members can edit the household
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.members.filter(member=request.user).exists()


class IsTaskGiverOrReadOnly(permissions.BasePermission):
    """
    Makes sure that only taskgivers han edit all fields of a task
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.task_giver.member == request.user
