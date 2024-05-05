from rest_framework.filters import OrderingFilter

from common import utils


class KeywordOrderingFilter(OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        sort = request.query_params.get('sort')

        if ordering:
            new_ordering = []
            for field in ordering:

                snake_case_field = utils.camel_to_snake(field)

                if sort == 'desc':
                    new_ordering.append(f"-{snake_case_field}")
                else:
                    new_ordering.append(f"{snake_case_field}")

            queryset = queryset.order_by(*new_ordering)

        return queryset