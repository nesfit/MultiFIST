from django.urls import path

from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='tasks'),
    path('new', views.TaskCreate.as_view(), name='task_create'),
    path('resume/<str:name>', views.resume, name='task_resume'),
    path('pause/<str:name>', views.pause, name='task_pause'),
    path('<int:pk>', views.TaskDetailView.as_view(), name='task'),
    path('edit/<int:pk>', views.TaskUpdate.as_view(), name='task_edit'),
    path('delete/<int:pk>', views.TaskDelete.as_view(), name='task_delete'),
    path('<int:task_pk>/<int:pk>', views.WebArchiveDetail.as_view(), name='web_archive_detail'),
]
