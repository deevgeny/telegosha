from django.urls import path

from .views import (
    UserProgressVeiw,
    UserTaskListView,
    UserTaskUpdateView,
    hello,
)

urlpatterns = [
    path('tasks/', hello, name='hello'),
    path('progress/<int:tg_id>/', UserProgressVeiw.as_view(),
         name='user-progress'),
    path('tasks/<int:tg_id>/', UserTaskListView.as_view(),
         name='user-tasks-list'),
    path('tasks/<int:tg_id>/<int:task_id>/',
         UserTaskUpdateView.as_view(),
         name='update-user-task')
]
