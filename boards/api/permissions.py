from rest_framework import permissions
from boards.models import Boards


class IsBoardOwnerOrMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        is_owner = obj.owner == user
        is_member = obj.members.filter(pk=user.id).exists()

        return is_owner or is_member
    

class IsBoardOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        is_owner = obj.owner == user

        return is_owner