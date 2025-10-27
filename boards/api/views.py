from rest_framework import viewsets
from rest_framework.response import Response
from boards.models import Boards
from .serializers import BoardsSeralizer, BoardDetailSerializer, BoardUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .permissions import IsBoardOwnerOrMember, IsBoardOwner
from django.db.models import Q



class BoardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing boards.
    Provides different serializers and permissions depending on the request type and action.
    """
    queryset = Boards.objects.all()
    serializer_class = BoardsSeralizer
    authentication_classes = [TokenAuthentication]
    permission_classes =[IsAuthenticated, IsBoardOwnerOrMember]


    def get_queryset(self):
        """
        Returns the queryset of boards.
        For 'retrieve' action, it prefetches related tasks and users.
        Otherwise, returns boards where the user is owner or member.
        """
        user = self.request.user

        if self.action == 'retrieve':
            return Boards.objects.prefetch_related(
                "tasks__assignee", "tasks__reviewer"
            )
        
        if self.action == 'list':
            return Boards.objects.filter(
                    Q(owner=user) | Q(members=user)
                ).distinct()

        return Boards.objects.all()
        
    
    def get_permissions(self):
        """
        Applies permission rules based on the request method:
        - POST: any authenticated user
        - DELETE: only board owner
        - Other: board owner or member
        """
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsBoardOwner()]
        
        return [IsAuthenticated(), IsBoardOwnerOrMember()]

    
    def get_serializer_class(self, *args, **kwargs):
        """
        Chooses the appropriate serializer class depending on the action:
        - retrieve → BoardDetailSerializer
        - update/patch → BoardUpdateSerializer
        - default → BoardsSerializer
        """
        if self.action == "retrieve":
            return BoardDetailSerializer
        if self.request.method in ("PUT", "PATCH"):
            return BoardUpdateSerializer
        return BoardsSeralizer
    
    def perform_update(self, serializer):
        """
        Updates the board's member list when performing an update.
        """
        members = serializer.validated_data.get('members_data')

        serializer.instance.members.set(members)
        return super().perform_update(serializer)
    


