import rest_framework_filters
from rest_framework_filters.filterset import FilterSetMetaclass


class FilterSetNkg(rest_framework_filters.FilterSet, metaclass=FilterSetMetaclass):

    def filter_queryset(self, queryset):
        """
        Provide support for:

        ``view.fieldset_computed_fields``

        """
        qs = super().filter_queryset(queryset)

        computed_fields = getattr(self.Meta, 'computed_fields', None)
        if computed_fields is not None:
            # if computed_fields was provided, filter by them
            for cfn in computed_fields.keys():
                cf = computed_fields.get(cfn)
                for s in cf:
                    if s == 'exact':
                        lookup = cfn
                    else:
                        lookup = '%s__%s' % (cfn, s)
                    value = self.request.query_params.get(lookup)
                    if value is not None:
                        qs = qs.filter(**{lookup: value})

        return qs
