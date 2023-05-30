from rest_framework.routers import DefaultRouter

from schedule.views import (TeacherViewSet, SubjectViewSet, ScheduleViewSet,
                            SemesterViewSet, TaskViewSet, AttendanceView,
                            EvaluateMethodSubjectView, GradeViewSet
                            )

router = DefaultRouter(trailing_slash=False)
router.register(r'teachers', TeacherViewSet)
router.register(r"subjects", SubjectViewSet)
router.register(r"schedules", ScheduleViewSet)
router.register(r'semesters', SemesterViewSet)
router.register(r'evaluate-methods', EvaluateMethodSubjectView)
router.register(r'tasks', TaskViewSet)
router.register(r'attendances', AttendanceView)
router.register(r'grades', GradeViewSet)

urlpatterns = []

urlpatterns += router.urls
