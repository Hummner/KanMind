from django.urls import path, include
from rest_framework_nested import routers
from .views import TasksViewSet, TaskAssignedToUserView, TaskReviewerView, CommentsView

router = routers.SimpleRouter()
router.register(r'', TasksViewSet)

comments_router = routers.NestedSimpleRouter(router, r'', lookup='task')
comments_router.register(r'comments', CommentsView)



urlpatterns = [
    path('assigned-to-me/', TaskAssignedToUserView.as_view()),
    path('reviewer/', TaskReviewerView.as_view()),
    path('', include(router.urls)),
    path('', include(comments_router.urls))
    
]