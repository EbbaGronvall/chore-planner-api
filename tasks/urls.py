from django.urls import path
from tasks import views

urlpatterns =  [
    path('tasks/', views.TaskList.as_view()),
    # path('profiles/<int:pk>/', views.ProfileDetail.as_view()),
]