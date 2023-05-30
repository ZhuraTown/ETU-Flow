import os
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from etu_flow_api.settings import STATIC_ROOT
from users.serializers import (MyTokenObtainPairSerializer, UserETUSerializer,
                               UserETUUpdateSerializer, UserETUUpdateAdminSerializer, StudentsUploadSerializer)
from users.filters import UsersETUFilter
from users.permissions import UserIsAdmin, StudentIsLead, IsOwnerProfile
from users.models import UserETU
from university_structure.models import Group


class UserETUViewSet(mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet,
                     ):
    queryset = UserETU.objects.all()
    serializer_class = UserETUSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = UsersETUFilter

    def get_permissions(self):
        if self.action in ["destroy", "create", "retrieve", "invite_user", "list"]:
            self.permission_classes = [IsAuthenticated,  (UserIsAdmin | StudentIsLead)]
        if self.action in ['update_me']:
            self.permission_classes = [IsAuthenticated, IsOwnerProfile]
        if self.action in ["update"]:
            self.permission_classes = [IsAuthenticated, UserIsAdmin]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['update_me']:
            return UserETUUpdateSerializer
        if self.action in ["update"]:
            return UserETUUpdateAdminSerializer
        return super().get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        data = {"msg": f"Пользователь с id: {kwargs.pop('pk')} успешно удален."}
        return Response(status=status.HTTP_204_NO_CONTENT, data=data)

    @action(detail=False, methods=["put"])
    def update_me(self, request):
        instance = request.user
        serializer = self.get_serializer(data=request.data, instance=instance, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def invite_user(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class UserAuthView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class DownloadStudentsTemplateView(GenericAPIView):
    serializer_class = StudentsUploadSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = [IsAuthenticated, (UserIsAdmin | StudentIsLead)]

    def get(self, request, *args, **kwargs):
        path = 'upload_students_template.xlsx'
        with open(os.path.join(STATIC_ROOT, path), "rb") as excel:
            data = excel.read()

        response = HttpResponse(data)
        response['Content-Type'] = 'application/vnd.ms-excel'
        response['Content-Disposition'] = 'attachment; filename="' + path + '"'
        return response


class UploadStudentsView(mixins.CreateModelMixin, GenericAPIView):
    serializer_class = StudentsUploadSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = [IsAuthenticated, (UserIsAdmin | StudentIsLead)]

    def post(self, request, *args, **kwargs):
        self.request.data['group'] = get_object_or_404(Group, id=kwargs.get("group"))
        return self.create(request, *args, **kwargs)


