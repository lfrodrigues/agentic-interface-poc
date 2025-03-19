from django.urls import path
from .views import TalkAgentView

urlpatterns = [
    path('', TalkAgentView.as_view(), name='talk-agent'),
] 