"""metricBA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from rest_framework import routers
from metricBA_apps import views
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from restful.business.views import storage, overview, users, top, cpu, memory, network, ranking

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Create our schema's view w/ the get_schema_view() helper method. Pass in the proper Renderers for swagger
schema_view = get_schema_view(title='Metric_report API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^home/$', overview, name='home'),
    url(r'^overview/index.html', overview, name='overview'),
    url(r'^storage/index.html', storage, name='storage'),
    url(r'^top/index.html', top, name='top'),
    url(r'^users/index.html', users, name='users'),
    url(r'^iframes/cpu.html', cpu, name='cpu'),
    url(r'^iframes/memory.html', memory, name='memory'),
    url(r'^iframes/network.html', network, name='network'),
    url(r'^iframes/ranking.html', ranking, name='ranking'),
    url('^$', overview, name="docs"),
    url('^docs/$', schema_view, name="docs"),
    url(r'^admin/', admin.site.urls),
    url(r'^api/users/', include('metricBA_apps.urls')),
    url(r'^api/', include('restful.business.urls')),
    # url(r'^', include(router.urls)),
    url(r'^api/v1/celery-inspect/', include('celery_inspect.urls', namespace='celery_inspect')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
