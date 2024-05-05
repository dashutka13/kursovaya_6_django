from django.urls import path

from emailing.apps import EmailingConfig
from emailing.views import EmailingListView, EmailingCreateView, EmailingUpdateView, EmailingDeleteView, \
    EmailingDetailView, ClientListView, ClientCreateView, ClientUpdateView, ClientDetailView, \
    ClientDeleteView, Text_MessagesListView, Text_MessagesCreateView, Text_MessagesDetailView, Text_MessagesUpdateView, Text_MessagesDeleteView

app_name = EmailingConfig.name

urlpatterns = [
    path('', EmailingListView.as_view(), name='emailing_list'),
    path('emailing_create/', EmailingCreateView.as_view(), name='create_emailing'),
    path('emailing/<int:pk>/detail/', EmailingDetailView.as_view(), name='emailing_detail'),
    path('emailing/<int:pk>/update/', EmailingUpdateView.as_view(), name='emailing_update'),
    path('emailing/<int:pk>/delete/', EmailingDeleteView.as_view(), name='emailing_delete'),
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/detail/', ClientDetailView.as_view(), name='client_detail'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('message_list', Text_MessagesListView.as_view(), name='message_list'),
    path('message_create/', Text_MessagesCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/detail/', Text_MessagesDetailView.as_view(), name='message_detail'),
    path('message/<int:pk>/update/', Text_MessagesUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', Text_MessagesDeleteView.as_view(), name='message_delete'),

]
