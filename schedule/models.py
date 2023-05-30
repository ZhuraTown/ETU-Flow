import enum
from django.db import models


class Subject(models.Model):
    title = models.CharField(max_length=256)


class Teacher(models.Model):

    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    middle_name = models.CharField(max_length=128, null=True)
    profile_image = models.ImageField(upload_to="teachers/", null=True)
    number = models.CharField(max_length=12, null=True)
    email = models.EmailField(max_length=128, null=True)
    subjects = models.ManyToManyField(Subject, verbose_name="Предметы", related_name="teachers", blank=True)


class Semester(models.Model):
    date_start = models.DateField()
    date_end = models.DateField()
    title = models.CharField(max_length=256)
    is_deleted = models.BooleanField(default=False)
    subjects = models.ManyToManyField(Subject, verbose_name="Предметы", related_name="semesters", blank=True)


class Schedule(models.Model):

    class DaysOfWeek(enum.Enum):
        MONDAY = 1
        TUESDAY = 2
        WEDNESDAY = 3
        THURSDAY = 4
        FRIDAY = 5
        SATURDAY = 6
        SUNDAY = 7

        @classmethod
        def to_choices(cls):
            return [(en.value, en.value) for en in cls]

    class EventType(models.TextChoices):
        LECTURE = 0
        PRACTICE = 1

    is_even = models.BooleanField(verbose_name="Четная неделя", default=False)
    is_deleted = models.BooleanField(verbose_name='Запись удалена', default=False)
    time_start = models.TimeField(verbose_name="Начало лекции")
    time_end = models.TimeField(verbose_name="Конец лекции")
    day_of_week = models.CharField(verbose_name="День недели", choices=DaysOfWeek.to_choices(), max_length=64)
    group = models.ForeignKey("university_structure.Group", on_delete=models.CASCADE,
                              related_name="schedules", null=True)
    semester = models.ForeignKey("Semester", on_delete=models.CASCADE, related_name="schedules")
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE, related_name="schedules")
    auditorium = models.CharField(verbose_name="Аудитория", max_length=128, blank=True)
    event_type = models.CharField(verbose_name="Лекция/практика", max_length=64,
                                  choices=EventType.choices, default=EventType.LECTURE)


class Task(models.Model):

    date_created = models.DateTimeField(auto_now=True)
    content = models.TextField()
    date_of_completion = models.DateField()
    is_finished = models.BooleanField(default=False)
    author = models.ForeignKey("users.UserETU", on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="tasks")
    group = models.ForeignKey("university_structure.Group", on_delete=models.CASCADE, related_name="tasks")
    image = models.ImageField(upload_to="tasks/", null=True)


class Attendance(models.Model):

    date = models.DateField(verbose_name="Дата посещения")
    time = models.TimeField(verbose_name='Время посещения')
    presents = models.BooleanField(verbose_name="Присутствие")
    user = models.ForeignKey("users.UserETU", on_delete=models.CASCADE, related_name="attendances")
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE)


class EvaluateMethodSubject(models.Model):

    class EvaluateTypes(models.TextChoices):
        EXAM = 'exam'  # экзамен
        OFFSET = "offset"  # зачет

    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="evaluation_methods")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="evaluation_methods")
    group = models.ForeignKey("university_structure.Group", on_delete=models.CASCADE, related_name="evaluation_methods")
    evaluation_method = models.CharField(max_length=16, choices=EvaluateTypes.choices, default=EvaluateTypes.EXAM)


class Grade(models.Model):

    class GradeTypes(models.TextChoices):
        PASS = "pass"
        NOT_PASS = "not_pass"
        EXCELLENT = "excellent"
        GOOD = "good"
        SATISFACTORY = "satisfactory"

    grade = models.CharField(max_length=64, choices=GradeTypes.choices)
    intermediate_certification = models.BooleanField(verbose_name="Промежуточная аттестация", blank=True, null=True)
    user = models.ForeignKey("users.UserETU", on_delete=models.CASCADE, related_name="grades")
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE, related_name="grades")
    semester = models.ForeignKey("Semester", on_delete=models.CASCADE)

