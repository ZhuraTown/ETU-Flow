import django_filters
from django_filters import rest_framework

from university_structure.models import Group, Department, News, Faculty


class GroupFilter(django_filters.FilterSet):
    name = rest_framework.CharFilter(field_name="name", lookup_expr="contains")
    department__name = rest_framework.CharFilter(field_name="department__name", lookup_expr="contains")
    department__pk = rest_framework.NumberFilter(field_name="department__pk")

    class Meta:
        model = Group
        fields = ["name"]


class DepartmentFilter(django_filters.FilterSet):
    name = rest_framework.CharFilter(field_name="name")
    faculty__pk = rest_framework.NumberFilter(field_name="faculty__pk")
    faculty__name = rest_framework.CharFilter(field_name='faculty__name', lookup_expr="contains")

    class Meta:
        model = Department
        fields = ["name"]


class FacultyFilter(django_filters.FilterSet):
    name = rest_framework.CharFilter(field_name="name", lookup_expr="contains")

    class Meta:
        model = Faculty
        fields = ["name"]


class NewsFilter(django_filters.FilterSet):
    title = rest_framework.CharFilter(field_name="title", lookup_expr="icontains")
    date_create__gte = rest_framework.DateTimeFilter(field_name="date_created", lookup_expr="gte")
    date_create__lte = rest_framework.DateTimeFilter(field_name="date_created", lookup_expr="lte")
    faculty__pk = rest_framework.NumberFilter(field_name="faculty__pk")
    author__pk = rest_framework.NumberFilter(field_name="author__pk")

    class Meta:
        model = News
        fields = ["title", "date_created"]

