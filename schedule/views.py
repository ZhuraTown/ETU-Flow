from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

from schedule.filters import (TaskFilter, SemesterFilter, SubjectFilter,
                              TeacherFilter, ScheduleFilter, AttendanceFilter, EvaluateMethodSubjectFilter, GradeFilter)
from schedule.models import Teacher, Subject, Semester, Schedule, Task, Attendance, EvaluateMethodSubject, Grade
from schedule.serializers import (TeacherSerializer, TeacherUpdateSerializer, SubjectSerializer,
                                  ScheduleSerializer, ScheduleRetrieveSerializer,
                                  SemesterCreateUpdateSerializer, SemesterRetrieveSerializer,
                                  TaskCreateSerializer, TaskRetrieveSerializer, TaskUpdateSerializer,
                                  AttendanceSerializer, AttendanceRetrieveSerializer,
                                  EvaluateMethodSubjectRetrieveSerializer, EvaluateMethodSubjectSerializer,
                                  GradeRetrieveSerializer, GradeSerializer, GradeUpdateSerializer,
                                  )
from users.permissions import UserIsAdmin, StudentIsLead


class AbstractViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, UserIsAdmin]
        return super().get_permissions()


class TeacherViewSet(AbstractViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeacherFilter

    def get_serializer_class(self):
        if self.action in ['update']:
            return TeacherUpdateSerializer
        return super().get_serializer_class()


class SubjectViewSet(AbstractViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubjectFilter


class ScheduleViewSet(AbstractViewSet):
    queryset = Schedule.objects.filter(is_deleted=False)
    serializer_class = ScheduleRetrieveSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ScheduleFilter

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return ScheduleSerializer
        return super().get_serializer_class()


class SemesterViewSet(AbstractViewSet):
    queryset = Semester.objects.filter(is_deleted=False)
    serializer_class = SemesterRetrieveSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SemesterFilter

    def get_serializer_class(self):
        if self.action in ['create', "update"]:
            return SemesterCreateUpdateSerializer
        return super().get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        return Response(status=status.HTTP_204_NO_CONTENT)


class EvaluateMethodSubjectView(AbstractViewSet):
    queryset = EvaluateMethodSubject.objects.all()
    serializer_class = EvaluateMethodSubjectRetrieveSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EvaluateMethodSubjectFilter

    def get_serializer_class(self):
        if self.action in ['create', "update"]:
            return EvaluateMethodSubjectSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action not in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, UserIsAdmin]
        return super().get_permissions()


class TaskViewSet(AbstractViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskRetrieveSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return TaskCreateSerializer
        elif self.action in ['update']:
            return TaskUpdateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create', "update"]:
            self.permission_classes = [IsAuthenticated, (StudentIsLead | UserIsAdmin)]
        return super().get_permissions()


class AttendanceView(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    queryset = Attendance.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceRetrieveSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AttendanceFilter

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, (StudentIsLead | UserIsAdmin)]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ["create"]:
            return AttendanceSerializer
        return super().get_serializer_class()


class GradeViewSet(AbstractViewSet):
    queryset = Grade.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    serializer_class = GradeRetrieveSerializer
    filterset_class = GradeFilter

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, (StudentIsLead | UserIsAdmin)]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['create']:
            return GradeSerializer
        elif self.action in ['update']:
            return GradeUpdateSerializer
        return super().get_serializer_class()