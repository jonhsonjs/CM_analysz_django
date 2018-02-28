from django.http import JsonResponse
from rest_framework import permissions, generics, status
from rest_framework.response import Response

from metricBA_apps.models import UserGroup, StaffInfo
from metricBA_apps.serializers import UserGroupSerializer, StaffInfoSerializer
from restful.util.json_util import MetricJsonEncoder

from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class UserGroupMixin(object):
    model = UserGroup
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer


class UserGroupList(UserGroupMixin, generics.ListCreateAPIView):
    permission_classes = [
        permissions.AllowAny
    ]

    def get(self, request, *args, **kwargs):
        response = super(UserGroupList, self).get(request, *args, **kwargs)
        resp = JsonResponse({
            'status': 0,
            'data': response.data,
        }, encoder=MetricJsonEncoder, json_dumps_params={'ensure_ascii': False, 'indent': 4, 'encoding': "utf-8"})
        return resp

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            self.perform_create(serializer)
            data = {
                'status': 0,
                'data': serializer.data,
            }
            headers = self.get_success_headers(serializer.data)
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        data = {
            'status': 1,
            'message': serializer.errors,
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class UserGroupDetail(UserGroupMixin, generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        data = {
            'status': 0,
        }
        return Response(data, status=status.HTTP_200_OK)


class GroupStaffList(generics.ListCreateAPIView):
    model = StaffInfo
    queryset = StaffInfo.objects.all()
    serializer_class = StaffInfoSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, *args, **kwargs):
        response = super(GroupStaffList, self).get(request, *args, **kwargs)
        resp = JsonResponse({
            'status': 0,
            'data': response.data,
        }, encoder=MetricJsonEncoder, json_dumps_params={'ensure_ascii': False, 'indent': 4, 'encoding': "utf-8"})
        return resp

    def get_queryset(self):
        queryset = super(GroupStaffList, self).get_queryset()
        return queryset.filter(group__pk=self.kwargs.get('pk'))

    def perform_create(self, serializer):
        queryset = UserGroup.objects.all().filter(pk=self.kwargs.get('pk')).first()
        serializer.save(group=queryset)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            self.perform_create(serializer)
            data = {
                'status': 0,
                'data': serializer.data,
            }
            headers = self.get_success_headers(serializer.data)
            return Response(data, status=status.HTTP_201_CREATED, headers=headers)
        data = {
            'status': 1,
            'message': serializer.errors,
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class GroupStaffList1(generics.ListAPIView):
    model = StaffInfo
    queryset = StaffInfo.objects.all()
    serializer_class = StaffInfoSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, *args, **kwargs):
        response = super(GroupStaffList1, self).get(request, *args, **kwargs)
        resp = JsonResponse({
            'status': 0,
            'data': response.data,
        }, encoder=MetricJsonEncoder, json_dumps_params={'ensure_ascii': False, 'indent': 4, 'encoding': "utf-8"})
        return resp

    def get_queryset(self):
        queryset = super(GroupStaffList1, self).get_queryset()
        return queryset.filter(group__name=self.kwargs.get('name'))


class StaffMixin(object):
    model = StaffInfo
    queryset = StaffInfo.objects.all()
    serializer_class = StaffInfoSerializer
    permission_classes = [
        permissions.AllowAny
    ]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def perform_create(self, serializer):
        """Force author to the current user on save"""
        serializer.save(author=self.request.user)


class StaffList(StaffMixin, generics.ListCreateAPIView):
    pass


class StaffDetail(StaffMixin, generics.RetrieveUpdateDestroyAPIView):
    def delete(self, request, *args, **kwargs):
        rep = self.destroy(request, *args, **kwargs)
        data = {
            'status': 0,
        }
        return Response(data, status=status.HTTP_200_OK)

