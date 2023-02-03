from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response

from study.models import Task

from .serializers import ExerciseSerializer, TaskUpdateSerializer

User = get_user_model()


@api_view(['GET'])
def hello(request):
    return Response({'what': 'hi', 'params': request.query_params})


class UserTasksListView(ListAPIView):
    """User tasks list view."""

    serializer_class = ExerciseSerializer

    def get_queryset(self):
        tg_id = self.kwargs.get('tg_id')
        queryset = (get_object_or_404(User, tg_id=tg_id)
                    .exercises.filter(tasks__passed=False)
                    .prefetch_related('words'))
        return queryset


class UserTaskResultsUpdateView(UpdateAPIView):
    """User task results update view."""

    queryset = Task.objects.all()
    serializer_class = TaskUpdateSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user__tg_id=self.kwargs['tg_id'],
                                exercise=self.kwargs['excercise_id'])
        return obj
