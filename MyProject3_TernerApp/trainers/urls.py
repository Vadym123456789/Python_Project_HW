# trainers/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.trainer_list, name='trainer_list'),
    path('<int:pk>/', views.trainer_detail, name='trainer_detail'),
    path('<int:id>/<int:service_id>/', views.service_detail, name='service_detail'),
]
