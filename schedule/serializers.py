from rest_framework import serializers

from schedule.models import Schedule, Subject, Semester, Teacher, Task, Attendance, EvaluateMethodSubject, Grade
from university_structure.models import Group
from users.serializers import UserETUSerializer
from university_structure.serializers import GroupSerializer


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = (
                  "id",
                  "first_name",
                  "last_name",
                  "middle_name",
                  "profile_image",
                  "number",
                  "email",
                  "subjects"
                  )
        read_only_fields = ('id', )


class TeacherUpdateSerializer(TeacherSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    middle_name = serializers.CharField(required=False)


class SubjectSerializer(serializers.ModelSerializer):
    teachers = TeacherSerializer(many=True, required=False)

    class Meta:
        model = Subject
        fields = ("id",
                  "title",
                  "teachers")
        read_only_fields = ("id", "teachers")


class SemesterCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Semester
        fields = ("id",
                  "date_start",
                  "date_end",
                  "title",
                  "is_deleted",
                  "subjects",
                  )
        read_only_fields = ("id", "is_deleted")


class SemesterRetrieveSerializer(SemesterCreateUpdateSerializer):
    subjects = SubjectSerializer(many=True)


class TaskCreateSerializer(serializers.ModelSerializer):
    is_finished = serializers.BooleanField(required=False)

    class Meta:
        model = Task
        fields = ("id",
                  "date_created",
                  "content",
                  "date_of_completion",
                  "is_finished",
                  "image",
                  "author",
                  "subject",
                  "group",
                  )
        read_only_fields = ("id", "author")

    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user
        task = Task.objects.create(**validated_data)
        task.is_finished = False
        task.save()
        return task


class TaskUpdateSerializer(TaskCreateSerializer):
    content = serializers.CharField(required=False)
    date_of_completion = serializers.DateField(required=False)
    is_finished = serializers.BooleanField(required=False)
    image = serializers.ImageField(required=False)
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), required=False)
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), required=False)


class TaskRetrieveSerializer(TaskCreateSerializer):
    author = UserETUSerializer()
    subject = SubjectSerializer()
    group = GroupSerializer()


class ScheduleSerializer(serializers.ModelSerializer):
    day_of_week = serializers.IntegerField()

    class Meta:
        model = Schedule
        fields = ("id",
                  "is_even",
                  "time_start",
                  "time_end",
                  "day_of_week",
                  "group",
                  "semester",
                  "subject",
                  "event_type",
                  "auditorium",
                  )
        read_only_fields = ("id", )

    def validate(self, attrs):
        if attrs['time_start'] >= attrs['time_end']:
            raise serializers.ValidationError("time_start не может быть позже time_end")
        if Schedule.objects.filter(is_even=attrs['is_even'], day_of_week=attrs['day_of_week'],
                                   group=attrs['group'], semester=attrs['semester'], subject=attrs['subject'],
                                   time_start=attrs['time_start']):
            raise serializers.ValidationError(f"На это время уже существует расписание")
        return attrs


class ScheduleRetrieveSerializer(ScheduleSerializer):
    group = GroupSerializer()
    semester = SemesterRetrieveSerializer()
    subject = SubjectSerializer()


class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = ("id", "date", "time", "presents", "user", "subject")

    def validate(self, attrs):
        if Attendance.objects.filter(date=attrs['date'], user=attrs['user'],
                                     time=attrs['time'], subject=attrs['subject']):
            raise serializers.ValidationError("На указанный предмет, пользователя и дату уже существует посещение!")
        return attrs


class AttendanceRetrieveSerializer(AttendanceSerializer):
    user = UserETUSerializer()
    subject = SubjectSerializer()


class EvaluateMethodSubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = EvaluateMethodSubject
        fields = ["semester", "subject", "group", "evaluation_method"]


class EvaluateMethodSubjectRetrieveSerializer(EvaluateMethodSubjectSerializer):
    semester = SemesterCreateUpdateSerializer()
    subject = SubjectSerializer()
    group = GroupSerializer()


class GradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = ["id", "grade", "intermediate_certification", "user", "subject", "semester"]

    def validate(self, attrs):
        evaluating_method = EvaluateMethodSubject.objects.filter(semester=attrs['semester'], subject=attrs['subject']).first()

        if not evaluating_method:
            raise serializers.ValidationError("Нельзя ставить оценку по предмету, у которого нет метод оценивания!")

        if evaluating_method.evaluation_method == EvaluateMethodSubject.EvaluateTypes.EXAM:
            if attrs['grade'] not in [Grade.GradeTypes.EXCELLENT, Grade.GradeTypes.GOOD,
                                      Grade.GradeTypes.SATISFACTORY, Grade.GradeTypes.NOT_PASS]:
                raise serializers.ValidationError("Оценка не соответствует методу оценивания!")
        else:
            if attrs['grade'] not in [Grade.GradeTypes.NOT_PASS, Grade.GradeTypes.PASS]:
                raise serializers.ValidationError("Оценка не соответствует методу оценивания!")

        if Grade.objects.filter(user=attrs['user'], subject=attrs['subject'], semester=attrs['semester']):
            raise serializers.ValidationError("У пользователя уже есть оценка!")
        return attrs


class GradeRetrieveSerializer(GradeSerializer):
    user = UserETUSerializer()
    subject = SubjectSerializer()
    semester = SemesterCreateUpdateSerializer()


class GradeUpdateSerializer(serializers.ModelSerializer):
    grade = serializers.ChoiceField(choices=Grade.GradeTypes.choices, required=False)
    intermediate_certification = serializers.BooleanField(required=False)

    class Meta:
        model = Grade
        fields = ["id", "grade", "intermediate_certification", "user", "subject", "semester"]
        read_only_fields = ["user", "subject", "semester"]

    def validate_grade(self, value):
        grade = self.instance
        evaluating_method = EvaluateMethodSubject.objects.filter(semester=grade.semester, subject=grade.subject).first()
        if evaluating_method.evaluation_method == EvaluateMethodSubject.EvaluateTypes.EXAM:
            if value not in [Grade.GradeTypes.EXCELLENT, Grade.GradeTypes.GOOD,
                                      Grade.GradeTypes.SATISFACTORY, Grade.GradeTypes.NOT_PASS]:
                raise serializers.ValidationError("Оценка не соответствует методу оценивания!")
        else:
            if value not in [Grade.GradeTypes.NOT_PASS, Grade.GradeTypes.PASS]:
                raise serializers.ValidationError("Оценка не соответствует методу оценивания!")
        return value
