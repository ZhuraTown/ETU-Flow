import django_filters
from django_filters import rest_framework
from users.models import UserETU


class UsersETUFilter(django_filters.FilterSet):
    email = rest_framework.CharFilter(field_name="email", lookup_expr="icontains")
    first_name = rest_framework.CharFilter(field_name="first_name", lookup_expr="contains")
    last_name = rest_framework.CharFilter(field_name="last_name", lookup_expr="contains")
    middle_name = rest_framework.CharFilter(field_name="middle_name", lookup_expr="contains")
    user_type = rest_framework.ChoiceFilter(field_name="user_type", choices=UserETU.UserType.choices)
    group__title = django_filters.CharFilter(field_name="group__name", lookup_expr="icontains")
    group__pk = django_filters.NumberFilter(field_name="group__pk")
    is_staff = django_filters.BooleanFilter(field_name="is_staff")

    class Meta:
        model = UserETU
        fields = ["email", "user_type", "first_name", "last_name", "middle_name", "group", "is_staff"]
