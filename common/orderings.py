from rest_framework.filters import OrderingFilter


class KeywordOrderingFilter(OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        sort = request.query_params.get('sort')

        if ordering:
            new_ordering = []
            for field in ordering:
                if sort == 'desc':
                    new_ordering.append(f"-{field}")
                else:
                    new_ordering.append(f"{field}")

            queryset = queryset.order_by(*new_ordering)

        return queryset
