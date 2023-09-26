from django.urls import path
from django.views.decorators.cache import cache_page

from mailings.apps import MailingsConfig
from mailings.views import IndexView, MailingListView, MailingCreateView, MailingUpdateView, MailingDeleteView, \
    MailingDetailView, ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, LogsListView, \
    toggle_activity

app_name = MailingsConfig.name

urlpatterns = [
    path('', cache_page(180)(IndexView.as_view()), name='index'),
    path('mailings/', MailingListView.as_view(), name='mailings_list'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/detail/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('activity/<int:pk>/', toggle_activity, name='toggle_activity'),

    path('mailings/logs/<int:pk>/', LogsListView.as_view(), name='logs_list'),

    path('mailings/clients/', cache_page(180)(ClientListView.as_view()), name='clients_list'),
    path('mailings/clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('mailings/clients/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('mailings/clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),
]
