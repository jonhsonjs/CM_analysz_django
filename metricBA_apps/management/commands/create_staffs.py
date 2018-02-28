from django.core.management.base import BaseCommand

from metricBA_apps.models import UserGroup, StaffInfo

users = ['Bob', 'Sally', 'Joe', 'Rachel']


class Command(BaseCommand):
    def handle(self, *args, **options):
        groups = UserGroup.objects.all()

        for i, username in enumerate(users):
            StaffInfo.objects.create(group=groups[i % groups.count()], name=username, code=username, email="{}@example.com".format(username))
