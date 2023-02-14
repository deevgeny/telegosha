from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    ResultSerializer,
    ResultUpdateSerializer,
    TaskSerializer,
    UserProgressSerializer,
)
from study.models import Result

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
                            filter=Q(results__passed=True),
                            distinct=True),
                total_tasks=Count('results', distinct=True),
                passed_tasks=Count('results',
                                   filter=Q(results__passed=True),
                                   distinct=True)),
            tg_id=tg_id
        )
        serializer = UserProgressSerializer(progress)
        return Response(serializer.data)


class UserTasksListView(ListAPIView):
    """User tasks list view."""

    serializer_class = TaskSerializer

    def get_queryset(self):
        tg_id = self.kwargs.get('tg_id')
        return (get_object_or_404(User, tg_id=tg_id)
                .tasks.filter(results__passed=False)
                .prefetch_related('topic__words'))


class UserResultUpdateView(UpdateAPIView):
    """User task result update view."""

    queryset = Result.objects.all()
    serializer_class = ResultUpdateSerializer

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, user__tg_id=self.kwargs['tg_id'],
                                 task=self.kwargs['task_id'])


class UserResultsListView(ListAPIView):
    """User results list view."""

    serializer_class = ResultSerializer

    def get_queryset(self):
        return (Result.objects
                .filter(user__tg_id=self.kwargs['tg_id'])
                .select_related('task', 'task__topic'))
