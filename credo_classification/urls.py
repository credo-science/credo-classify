"""credo_classification URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework import routers

from classify.views import random_to_classify
from credo_classification.views import home
from database.views import ImportTeams, ImportCredoUsers, ImportDevices, ImportPings, ImportDetections
from definitions.views import AttributeViewSet
from users.views import obtain_auth_token, void_token, reset_password, auth_by_detector

router = routers.DefaultRouter()
router.register(r'attributes', AttributeViewSet)

urlpatterns = [
  path('admin/', admin.site.urls),
  url(r'^(?:index.html)?$', home, name='home'),
  url(r'^api-token-auth/', obtain_auth_token),
  url(r'^auth/', auth_by_detector),
  url(r'^api/logout/', void_token),
  url(r'^api/forgot/', reset_password),
  url(r'^api/import/teams/', ImportTeams.as_view()),
  url(r'^api/import/users/', ImportCredoUsers.as_view()),
  url(r'^api/import/devices/', ImportDevices.as_view()),
  url(r'^api/import/pings/', ImportPings.as_view()),
  url(r'^api/import/detections/', ImportDetections.as_view()),
  url(r'^api/classify/random/', random_to_classify),
  url(r'^api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [url(r'^(?P<path>.*)$', serve)]

urlpatterns = [
  url(r'^%s' % settings.BASE_URL, include(urlpatterns))
]
