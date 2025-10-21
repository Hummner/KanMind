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
    
    def list(self, request, *args, **kwargs):

        data = []
        for board in Boards.objects.all():
            tasks = board.tasks.all()
            ticket_count = len(tasks)
            tasks_to_do_count = len(board.tasks.filter(status='to-do'))
            tasks_high_prio_count = len(board.tasks.filter(priority='high'))

            data.append({
                'id': board.id,
                
            })

            




        return super().list(request,
                            ticket_count=ticket_count,
                            tasks_to_do_count = tasks_to_do_count,
                            tasks_high_prio_count = tasks_high_prio_count
                             *args, **kwargs)
    

    def perform_create(self, serializer):
        members = serializer.validated_data.get('members', [])
        serializer.save(
            member_count = len(members),
            owner_id = self.request.user,
        )



