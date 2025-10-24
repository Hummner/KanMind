from rest_framework import permissions
from boards.models import Boards


class IsBoardOwnerOrMember(permissions.BasePermission):

    def has_permission(self, request, view):
        

        user = request.user
        is_owner = user.owner_board.get(pk=user.id)
        is_member = user.members_board.get(pk=user.id)

        if is_owner and is_member:
            return True


        return False