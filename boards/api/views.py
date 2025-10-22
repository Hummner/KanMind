from rest_framework import viewsets
from rest_framework.response import Response
from boards.models import Boards
from .serializers import BoardsSeralizer, BoardDetailSerializer, BoardUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication



class BoardViewSet(viewsets.ModelViewSet):
    queryset = Boards.objects.all()
    serializer_class = BoardsSeralizer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get_queryset(self):

        if self.action == 'retrieve':
            return Boards.objects.prefetch_related(
                "tasks__assignee", "tasks__reviewer"
            )

        return Boards.objects.all()
    
    def get_serializer_class(self, *args, **kwargs):
        if self.action == "retrieve":
            return BoardDetailSerializer
        if self.request.method in ("PUT", "PATCH"):
            print('Yoo')
            return BoardUpdateSerializer
        return BoardsSeralizer
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

