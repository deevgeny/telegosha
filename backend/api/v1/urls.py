from django.urls import path

from .views import UserTaskResultsUpdateView, UserTasksListView, hello

urlpatterns = [
    path('tasks/', hello, name='hello'),
    path('tasks/<int:tg_id>/', UserTasksListView.as_view(),
         name='user-tasks-list'),
    path('tasks/<int:tg_id>/<int:excercise_id>/',
         UserTaskResultsUpdateView.as_view(),
         name='update-user-task')
]
