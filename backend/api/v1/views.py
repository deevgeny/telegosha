from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response

from .serializers import ResultSerializer, TaskSerializer
from study.models import Result

User = get_user_model()


@api_view(['GET'])
def hello(request):
    return Response({'what': 'hi', 'params': request.query_params})


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
    serializer_class = ResultSerializer

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, user__tg_id=self.kwargs['tg_id'],
                                 task=self.kwargs['task_id'])
