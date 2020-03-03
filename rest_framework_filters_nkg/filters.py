import warnings

from django.utils.module_loading import import_string
from django_filters.rest_framework.filters import *  # noqa
from django_filters.rest_framework.filters import Filter, ModelChoiceFilter

ALL_LOOKUPS = '__all__'
