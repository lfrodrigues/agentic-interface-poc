from django.urls import path
from api.views import TalkAgentView, CreateUserView

urlpatterns = [
    path('talk/', TalkAgentView.as_view(), name='talk-agent'),
    path('users/create/', CreateUserView.as_view(), name='create-user'),
] 