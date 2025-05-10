from django.urls import path

from api.views import (
    CreateUserView,
    DeleteUserView,
    TalkAgentView,
    ListUsersView,
    CreateInvoiceView,
)

urlpatterns = [
    path('talk/', TalkAgentView.as_view(), name='talk-agent'),
    path('users/create/', CreateUserView.as_view(), name='create-user'),
    path('users/delete/<str:customer_id>/', DeleteUserView.as_view(), name='delete-user'),
    path('users/', ListUsersView.as_view(), name='list-users'),
    path('invoices/create/', CreateInvoiceView.as_view(), name='create-invoice'),
]
