from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt

from metricBA_apps.api import UserGroupList, UserGroupDetail, GroupStaffList, StaffList, StaffDetail, GroupStaffList1

userGroup_urls = [
    url(r'^/(?P<pk>[0-9a-zA-Z_-]+)/staffs$', GroupStaffList.as_view(), name='groupStaff-list'),
    url(r'^/name/(?P<name>[0-9a-zA-Z_-]+)/staffs$', GroupStaffList1.as_view(), name='groupStaff-list1'),
    url(r'^/(?P<pk>[0-9a-zA-Z_-]+)$', UserGroupDetail.as_view(), name='userGroup-detail'),
    url(r'^$', UserGroupList.as_view(), name='userGroup-list')
]

staff_urls = [
    url(r'^/(?P<pk>\d+)$', csrf_exempt(StaffDetail.as_view()), name='staff-detail'),
    url(r'^$', csrf_exempt(StaffList.as_view()), name='staff-list')
]

urlpatterns = [
    url(r'^staffs', include(staff_urls)),
    url(r'^staffGroups', include(userGroup_urls)),
]
