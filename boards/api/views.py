from rest_framework import viewsets
from rest_framework.response import Response
from boards.models import Boards
from .serializers import BoardsSeralizer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Boards.objects.all()
    serializer_class = BoardsSeralizer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        members = serializer.validated_data.get('members', [])
        print(self.request.user)
        serializer.save(
            member_count = len(members),
            owner_id = self.request.user,
        )

    def retrieve(self, request, *args, **kwargs):
        

        return super().retrieve(request, *args, **kwargs)

