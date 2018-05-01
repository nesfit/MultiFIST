from django.urls import path

from . import views

urlpatterns = [
    path('', views.RuleListView.as_view(), name='rule'),
    path('new/', views.RuleCreate.as_view(), name='rule_create'),
    path('<int:pk>', views.RuleUpdate.as_view(), name='rule_update'),
    path('<int:pk>/delete/', views.RuleDelete.as_view(), name='rule_delete'),
]
