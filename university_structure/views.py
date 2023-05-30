from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, status, filters
from rest_framework.permissions import IsAuthenticated

from university_structure.serializers import (GroupListSerializer, FacultySerializer,
                                              DepartmentSerializer, NewsSerializer,
                                              NewSerializerRetrieve, NewsUpdateSerializer,
                                              DepartmentRetriveSerializer, GroupSerializer,
                                              )

from university_structure.models import Group, Faculty, Department, News
from university_structure.filters import GroupFilter, DepartmentFilter, FacultyFilter, NewsFilter

from users.permissions import UserIsAdmin


class AbstractStructureView(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet
                            ):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]

    def get_permissions(self):
        if self.action in ['destroy', "create", "update"]:
            self.permission_classes = [IsAuthenticated, UserIsAdmin]
        return super().get_permissions()


class GroupViewSet(AbstractStructureView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    filterset_class = GroupFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return GroupListSerializer
        return super().get_serializer_class()


class FacultyViewSet(AbstractStructureView):
    serializer_class = FacultySerializer
    queryset = Faculty.objects.all()
    filterset_class = FacultyFilter


class DepartmentViewSet(AbstractStructureView):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    filterset_class = DepartmentFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return DepartmentRetriveSerializer
        return super().get_serializer_class()


class NewsViewSet(AbstractStructureView):
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    filterset_class = NewsFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return NewSerializerRetrieve
        if self.action in ["update"]:
            return NewsUpdateSerializer
        return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

