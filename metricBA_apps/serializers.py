from django.contrib.auth.models import User, Group
from rest_framework import serializers

from metricBA_apps.models import UserGroup, StaffInfo


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class UserGroupSerializer(serializers.ModelSerializer):
    staffs = serializers.HyperlinkedIdentityField(view_name='groupStaff-list', lookup_field='pk')
    url = serializers.HyperlinkedIdentityField(view_name='userGroup-detail', lookup_field='pk')

    class Meta:
        model = UserGroup
        fields = ('id', 'url', 'name', 'description', 'create_user', 'join_date', 'staffs',)


class StaffInfoSerializer(serializers.ModelSerializer):
    group = UserGroupSerializer(required=False, read_only=True)

    def get_validation_exclusions(self, *args, **kwargs):
        # Need to exclude `user` since we'll add that later based off the request
        exclusions = super(StaffInfoSerializer, self).get_validation_exclusions(*args, **kwargs)
        return exclusions + ['group']

    class Meta:
        model = StaffInfo
        fields = '__all__'

