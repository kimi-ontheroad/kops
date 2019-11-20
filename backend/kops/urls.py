from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login', views.LoginView.as_view()),
    re_path('topics/', views.TopicView.as_view(), name='topic'),
    re_path('consumergroup/', views.ConsumerGroupView.as_view(), name='consumergroup'),
    re_path('monitor/', views.TopicMonitorView.as_view(), name='monitor')
]



