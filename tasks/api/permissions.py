from rest_framework import permissions


class IsMember(permissions.BasePermission):
    """
    Permission class that grants access only if the requesting user is a member of a board.
    """


    def has_permission(self, request, view):
        user = request.user
        is_member = user.members_board.filter(members=user).exists()

        return is_member
    
class IsTaskOrBoardOwner(permissions.BasePermission):
    """
    Permission class that allows access if the user is either the task owner or the board owner.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        is_task_owner = obj.owner == user
        is_board_owner = obj.board.owner == user

        return is_task_owner or is_board_owner


class IsCommentAuthor(permissions.BasePermission):
    """
    Permission class that allows access only if the user is the author of the comment.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        is_comment_author = obj.author == user


        return is_comment_author