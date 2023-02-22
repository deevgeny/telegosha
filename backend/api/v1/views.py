from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    TaskSerializer,
    TaskUpdateSerializer,
    UserProgressSerializer,
)
from study.models import Task

User = get_user_model()


@api_view(['GET'])
def hello(request):
    return Response({'what': 'hi', 'params': request.query_params})


class UserProgressVeiw(APIView):
    """User progress view."""
    def get(self, request, tg_id):
        progress = get_object_or_404(
            User.objects.annotate(
                topics=Count('tasks__topic', distinct=True),
                words=Count('tasks__topic__words',
                            filter=Q(tasks__passed=True),
                            distinct=True),
                total_tasks=Count('tasks', distinct=True),
                passed_tasks=Count('tasks',
                                   filter=Q(tasks__passed=True),
                                   distinct=True)),
            tg_id=tg_id
        )
        serializer = UserProgressSerializer(progress)
        return Response(serializer.data)


class UserTaskListView(ListAPIView):
    """User tasks list view."""

    serializer_class = TaskSerializer

    def get_queryset(self):
        tg_id = self.kwargs.get('tg_id')
        return (get_object_or_404(User, tg_id=tg_id)
                .tasks.filter(passed=False, active=True)
                .prefetch_related('topic__words'))


class UserTaskUpdateView(UpdateAPIView):
    """User task update view."""

    queryset = Task.objects.all()
    serializer_class = TaskUpdateSerializer

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, user__tg_id=self.kwargs['tg_id'],
                                 id=self.kwargs['task_id'])
