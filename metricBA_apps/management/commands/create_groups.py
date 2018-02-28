from django.core.management.base import BaseCommand

from metricBA_apps.models import UserGroup


class Command(BaseCommand):
    def handle(self, *args, **options):
        groups = ['group_1', 'group_2', 'group_3', 'group_4']
        for group in groups:
            group_name = group.lower()
            UserGroup.objects.create(name=group_name, description=group)
