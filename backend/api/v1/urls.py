from django.urls import path

from .views import (
    UserProgressVeiw,
    UserResultsListView,
    UserResultUpdateView,
    UserTasksListView,
    hello,
)

urlpatterns = [
    path('tasks/', hello, name='hello'),
    path('progress/<int:tg_id>/', UserProgressVeiw.as_view(),
         name='user-stats'),
    path('tasks/<int:tg_id>/', UserTasksListView.as_view(),
         name='user-tasks-list'),
    path('results/<int:tg_id>/', UserResultsListView.as_view(),
         name='user-results-list'),
    path('results/<int:tg_id>/<int:task_id>/',
         UserResultUpdateView.as_view(),
         name='update-user-result')
]
