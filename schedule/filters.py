import django_filters
from django_filters import rest_framework

from schedule.models import Task, Semester, Subject, Teacher, Schedule, Attendance, EvaluateMethodSubject, Grade


class TaskFilter(rest_framework.FilterSet):
    date_created__gte = django_filters.DateTimeFilter(field_name="date_created", lookup_expr='gte')
    date_created__lte = django_filters.DateTimeFilter(field_name="date_created", lookup_expr='lte')
    date_of_completion__gte = django_filters.DateFilter(field_name="date_of_completion", lookup_expr='gte')
    date_of_completion__lte = django_filters.DateFilter(field_name="date_of_completion", lookup_expr='lte')
    is_finished = django_filters.BooleanFilter(field_name="is_finished")

    class Meta:
        model = Task
        fields = ["date_created", "date_of_completion", "is_finished", "subject", "group"]


class SemesterFilter(rest_framework.FilterSet):
    date_start__gte = django_filters.DateFilter(field_name="date_start", lookup_expr='gte')
    date_start__lte = django_filters.DateFilter(field_name="date_start", lookup_expr='lte')
    date_end__gte = django_filters.DateFilter(field_name="date_end", lookup_expr='gte')
    date_end__lte = django_filters.DateFilter(field_name="date_end", lookup_expr='lte')
    title = django_filters.CharFilter(field_name="title", lookup_expr="contains")
    evaluation_method = django_filters.NumberFilter()

    class Meta:
        model = Semester
        fields = ["date_start", "date_end", "title"]


class EvaluateMethodSubjectFilter(rest_framework.FilterSet):
    semester__pk = django_filters.NumberFilter(field_name="semester__pk")
    group__pk = django_filters.NumberFilter(field_name="group__pk")
    subject = django_filters.NumberFilter(field_name="subject__pk")
    group__title = django_filters.CharFilter(field_name="group__title", lookup_expr="contains")
    subject__title = django_filters.CharFilter(field_name="subject__title", lookup_expr="contains")

    class Meta:
        model = EvaluateMethodSubject
        fields = ['semester', "group", "subject", "evaluation_method"]


class SubjectFilter(rest_framework.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="contains")
    evaluate_method = django_filters.ChoiceFilter(
        field_name="evaluation_methods__evaluation_method",
        choices=EvaluateMethodSubject.EvaluateTypes.choices,
        method="filter_evaluate_method"
    )
    group = django_filters.NumberFilter(field_name="evaluation_methods__group__pk", method="filter_group")
    semester = django_filters.NumberFilter(field_name="evaluation_methods__semester__pk", method="filter_semester")

    def filter_evaluate_method(self, queryset, name, value):
        return queryset.filter(evaluation_methods__evaluation_method=value)

    def filter_group(self, queryset, name, value):
        return queryset.filter(evaluation_methods__group=value)

    def filter_semester(self, queryset, name, value):
        return queryset.filter(evaluation_methods__semester=value)

    class Meta:
        model = Subject
        fields = ["title"]


class TeacherFilter(rest_framework.FilterSet):
    first_name = django_filters.CharFilter(field_name="first_name", lookup_expr="contains")
    last_name = django_filters.CharFilter(field_name="last_name", lookup_expr="contains")
    middle_name = django_filters.CharFilter(field_name="middle_name", lookup_expr="contains")
    email = django_filters.CharFilter(field_name="email", lookup_expr="contains")
    subjects__pk = django_filters.ModelMultipleChoiceFilter(
        field_name="subjects__pk",
        queryset=Subject.objects.all(),
        to_field_name="pk",
    )
    subjects__title = django_filters.CharFilter(field_name="subjects__title", lookup_expr="icontains")

    class Meta:
        model = Teacher
        fields = ["first_name", "last_name", "middle_name", "email"]


class ScheduleFilter(rest_framework.FilterSet):
    is_even = django_filters.BooleanFilter(field_name="is_even")
    time_start__gte = django_filters.TimeFilter(field_name="time_start", lookup_expr="gte")
    time_start__lte = django_filters.TimeFilter(field_name="time_start", lookup_expr="lte")
    time_end__gte = django_filters.TimeFilter(field_name="time_end", lookup_expr="gte")
    time_end__lte = django_filters.TimeFilter(field_name="time_end", lookup_expr="lte")
    day_of_week = django_filters.ChoiceFilter(field_name="day_of_week", choices=Schedule.DaysOfWeek.to_choices())
    group__name = django_filters.CharFilter(field_name="group__name", lookup_expr="icontains")
    group__pk = django_filters.NumberFilter(field_name="group__pk")
    semester = django_filters.NumberFilter(field_name="semester__id")
    subject__title = django_filters.CharFilter(field_name="subject__title", lookup_expr="icontains")
    subject__pk = django_filters.NumberFilter(field_name="subject__pk")

    class Meta:
        model = Schedule
        fields = ["is_even", "time_start", "time_end", "day_of_week", "group",
                  "semester", "subject", "auditorium", "event_type"]


class AttendanceFilter(django_filters.FilterSet):
    group__pk = rest_framework.NumberFilter(field_name="user__group__pk")
    group__title = rest_framework.CharFilter(field_name="user__group__name", lookup_expr="icontains")
    date__gte = rest_framework.DateFilter(field_name="date", lookup_expr="gte")
    date__lte = rest_framework.DateFilter(field_name="date", lookup_expr="lte")
    time__gte = rest_framework.TimeFilter(field_name="time", lookup_expr="gte")
    time__lte = rest_framework.TimeFilter(field_name="time", lookup_expr="lte")
    subject__pk = rest_framework.NumberFilter(field_name="subject__pk")
    subject__title = rest_framework.CharFilter(field_name="subject__title", lookup_expr="icontains")

    class Meta:
        model = Attendance
        fields = ["date", "user", "presents"]


class GradeFilter(django_filters.FilterSet):
    group__pk = django_filters.NumberFilter(field_name="user__group__pk")

    class Meta:
        model = Grade
        fields = ['user', "grade", "semester", "subject"]
