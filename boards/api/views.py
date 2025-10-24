from rest_framework import viewsets
from rest_framework.response import Response
from boards.models import Boards
from .serializers import BoardsSeralizer, BoardDetailSerializer, BoardUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .permissions import IsBoardOwnerOrMember, IsBoardOwner
from django.db.models import Q



class BoardViewSet(viewsets.ModelViewSet):
    queryset = Boards.objects.all()
    serializer_class = BoardsSeralizer
    authentication_classes = [TokenAuthentication]


    def get_queryset(self):
        user = self.request.user

        if self.action == 'retrieve':
            return Boards.objects.prefetch_related(
                "tasks__assignee", "tasks__reviewer"
            )
        
        return Boards.objects.filter(
                Q(owner=user) | Q(members=user)
            ).distinct()
        
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        
        if self.request.method == 'DELETE':
            return [IsAuthenticated(), IsBoardOwner()]
        
        return [IsAuthenticated(), IsBoardOwnerOrMember()]

    
    def get_serializer_class(self, *args, **kwargs):
        if self.action == "retrieve":
            return BoardDetailSerializer
        if self.request.method in ("PUT", "PATCH"):
            return BoardUpdateSerializer
        return BoardsSeralizer
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

