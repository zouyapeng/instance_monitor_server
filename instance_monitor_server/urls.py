"""instance_monitor_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
# from contact.views import ContactViewSet
from trigger.views import TriggerListView, TriggerCreateView, TriggerRetrieveUpdateDestroyView, EventListView
from heartbeat.views import MonitorAgentCreateView
from heartbeat.views import InstanceUUIDRetrieveView
from data.views import DataListView
from contact.views import ContactListView, ContactCreateView, ContactRetrieveUpdateDestroyView

# contact_list = ContactViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
#
# contact_detail = ContactViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'delete': 'destroy'
# })


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^heartbeat/$', MonitorAgentCreateView.as_view(), name='heartbeat'),

    url(r'^uuid/(?P<pk>[0-9]+)/$', InstanceUUIDRetrieveView.as_view(), name='instanceuuid-detail'),

    url(r'^contact/$', ContactListView.as_view(), name='contact-list'),
    url(r'^contact/(?P<pk>[0-9]+)/$', ContactRetrieveUpdateDestroyView.as_view(), name='contact-detail'),
    url(r'^contact-create/$', ContactCreateView.as_view(), name='contact-create'),

    url(r'^trigger/$', TriggerListView.as_view(), name='trigger-list'),
    url(r'^trigger/(?P<pk>[0-9]+)/$', TriggerRetrieveUpdateDestroyView.as_view(), name='trigger-detail'),
    url(r'^trigger-create/$', TriggerCreateView.as_view(), name='trigger-create'),

    url(r'^event/$', EventListView.as_view(), name='event-list'),

    url(r'^data/$', DataListView.as_view(), name='data-list'),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
