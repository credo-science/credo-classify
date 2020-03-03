from rest_framework.filters import OrderingFilter
from rest_framework_filters.backends import RestFrameworkFilterBackend, ComplexFilterBackend

from rest_framework_filters_nkg.filterset import FilterSetNkg
from rest_framework_filters_nkg.utils import *


parent_fields = ['ForeignField', 'PrimaryKeyRelatedField']
number_fields = ['IntegerField', 'FloatField', 'DateField', 'DateTimeField', 'BooleanField']
string_fields = ['CharField', 'TextField', 'ChoiceField']


class ComplexFilterNkgBackend(ComplexFilterBackend):
    """
    Extends for support of:

    ``view.filterset_fields = '__all__'`` - for extract filterset_fields from serializer or model (if serializer is None)
    ``view.filterset_extra_fields`` = {field: [lookups]} - for add extra fieldset ie. related fields
    ``view.computed_filter_fields`` = [field_name_list] - for computed field, added to queryset by annotation or extra method
    """
    filterset_base = FilterSetNkg

    def get_filterset_class(self, view, queryset=None):
        filterset_class = getattr(view, 'filterset_class', None)
        filterset_fields = getattr(view, 'filterset_fields', None)
        annotated_fields = {}
        fields = {}

        if filterset_class is not None:
            return super().get_filterset_class(view, queryset)

        if filterset_fields != '__all__':
            return super().get_filterset_class(view, queryset)

        if queryset is not None:
            MetaBase = getattr(self.filterset_base, 'Meta', object)
            model = queryset.model

            # Get serializer class
            if hasattr(view, 'get_serializer_class'):
                try:
                    serializer_class = view.get_serializer_class()
                except AssertionError:
                    serializer_class = None
            else:
                serializer_class = getattr(view, 'serializer_class', None)

            if serializer_class is None:
                # Extract fields names and types from model
                for f in model._meta.get_fields():
                    fields[f.get_attname()] = f.get_internal_type()
            else:
                # Extract fields names and types from serializer
                for name, f in serializer_class(context={}).fields.fields.items():
                    if not f.write_only:
                        fields[name] = type(f).__name__

            model_fields = {}
            extra_filter_fields = getattr(view, 'filterset_extra_fields', {})
            computed_filter_fields = getattr(view, 'filterset_computed_fields', [])
            filterset_ignore = getattr(view, 'filterset_ignore', [])

            # sort fields from serializer/model by model or computed and assign lookups by value type
            for name, field_type in fields.items():
                if name in filterset_ignore:
                    continue
                elif name in computed_filter_fields:
                    dest = annotated_fields
                else:
                    dest = model_fields

                if field_type in parent_fields:
                    dest[name] = parent_lokup
                if field_type in number_fields:
                    dest[name] = number_lokups
                if field_type in string_fields:
                    dest[name] = string_lokups

            # append extra fields and sort by model or computed
            for name, fl in extra_filter_fields.items():
                if name in computed_filter_fields:
                    dest = annotated_fields
                else:
                    dest = model_fields
                dest[name] = fl

            # make filter
            class AutoFilterSet(self.filterset_base):
                class Meta(MetaBase):
                    model = queryset.model
                    fields = model_fields
                    computed_fields = annotated_fields

            return AutoFilterSet

        return None
