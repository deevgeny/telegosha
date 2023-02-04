from django.urls import path

from .views import UserResultUpdateView, UserTasksListView, hello

urlpatterns = [
    path('tasks/', hello, name='hello'),
    path('tasks/<int:tg_id>/', UserTasksListView.as_view(),
         name='user-tasks-list'),
    path('tasks/<int:tg_id>/<int:task_id>/',
         UserResultUpdateView.as_view(),
         name='update-user-result')
]
