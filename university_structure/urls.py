from rest_framework.routers import DefaultRouter
from university_structure.views import GroupViewSet, FacultyViewSet, DepartmentViewSet, NewsViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r"groups", GroupViewSet)
router.register(r"faculties", FacultyViewSet)
router.register(r"departments", DepartmentViewSet)
router.register(r"news", NewsViewSet)

urlpatterns = router.urls
