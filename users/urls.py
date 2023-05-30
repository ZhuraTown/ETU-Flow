from django.urls import re_path, path
from rest_framework.routers import DefaultRouter

from users.views import UserETUViewSet, UserAuthView, DownloadStudentsTemplateView, UploadStudentsView

router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserETUViewSet)

urlpatterns = [
    re_path(r'users/auth?$', UserAuthView.as_view(), name='auth'),
    re_path(r"users/download_students", DownloadStudentsTemplateView.as_view(), name="download_template"),
    path("users/<int:group>/upload_students", UploadStudentsView.as_view(), name="upload_template"),
]

urlpatterns += router.urls
