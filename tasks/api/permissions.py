from rest_framework import permissions


class IsMember(permissions.BasePermission):


    def has_permission(self, request, view):
        user = request.user
        is_member = user.members_board.filter(user=user).exists()

        return is_member
    
