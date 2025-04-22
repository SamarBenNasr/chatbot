from django.urls import path
from . import views



urlpatterns = [
    path('', views.main, name='main'),
    path("api/chat/",views.chatbot_api, name="chatbot_api"),
]