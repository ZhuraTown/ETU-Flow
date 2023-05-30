from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from university_structure.models import Group, Faculty, News, Department
from users.serializers import UserETUSerializer


class FacultySerializer(serializers.ModelSerializer):

    class Meta:
        model = Faculty
        fields = (
            "id",
            "name",
        )
        read_only_fields = ['id']


class NewsSerializer(serializers.ModelSerializer):
    faculty = serializers.PrimaryKeyRelatedField(queryset=Faculty.objects.all())

    class Meta:
        model = News
        fields = (
            "id",
            "title",
            "content",
            "date_created",
            "coin_reward",
            "image",
            "faculty"
        )
        read_only_fields = ['id', "date_created"]

    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user
        return super().create(validated_data)

    def validate_coin_reward(self, value):
        if value < 0:
            raise serializers.ValidationError("Количество монет не может быть отрицательным!")
        return value


class NewSerializerRetrieve(NewsSerializer):
    author = UserETUSerializer(read_only=True)
    faculty = FacultySerializer()

    class Meta:
        model = News
        fields = (
            "id",
            "title",
            "content",
            "date_created",
            "coin_reward",
            "image",
            "author",
            "faculty",
        )
        read_only_fields = ['id', "date_created", 'author']


class NewsUpdateSerializer(NewsSerializer):
    title = serializers.CharField(required=False, validators=[UniqueValidator(queryset=News.objects.all())])
    content = serializers.CharField(required=False)
    coin_reward = serializers.IntegerField(required=False)
    image = serializers.ImageField(required=False)


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = (
            "id",
            "name",
            "faculty"
        )
        read_only_fields = ['id']


class DepartmentRetriveSerializer(DepartmentSerializer):
    faculty = FacultySerializer()


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "department"
        )
        read_only_fields = ['id']


class GroupListSerializer(GroupSerializer):
    department = DepartmentRetriveSerializer()
