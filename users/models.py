import django
from django.db import models
from django.contrib.auth.models import AbstractUser
from university_structure.models import Group
from rest_framework import serializers


class UserETU(AbstractUser):

    class UserType(models.TextChoices):
        LEAD = "lead"
        STUDENT = "student"

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, null=True)
    user_type = models.CharField(choices=UserType.choices,
                                 verbose_name="Тип пользователя",
                                 default=UserType.STUDENT,
                                 max_length=20)
    middle_name = models.CharField(max_length=150,
                                   verbose_name="Отчество",
                                   blank=True)
    profile_image = models.ImageField(verbose_name="Аватар", blank=True, null=True)
    coin_balance = models.PositiveIntegerField(default=0)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="students", null=True, blank=False)
    phone_number = models.CharField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "last_name",
        "first_name",
    ]

    @classmethod
    def create_from_xlsx(cls, group, table):
        fields_mapping = []
        students = []
        for r_idx, cell_row, in enumerate(table[0]):
            row = [i.value for i in cell_row]
            if not any(row):
                continue
            if r_idx < 1:  # Create header and get required indexes of sheet's columns
                header = row
                continue

            dict_from_sheet = {}
            for cidx, col in enumerate(row):
                dict_from_sheet.update({header[cidx]: col})
            fields_mapping.append(dict_from_sheet)
            try:
                instance = UserETU.objects.create(group=group[0], email=dict_from_sheet['Почта'],
                                                  first_name=dict_from_sheet['Имя'],
                                                  last_name=dict_from_sheet['Фамилия'],
                                                  middle_name=dict_from_sheet['Отчество'],
                                                  phone_number=dict_from_sheet['Номер'],
                                                  coin_balance=dict_from_sheet['Лэткоины']
                                                  )
                instance.set_password(str(dict_from_sheet['Пароль']))
                instance.save()
            except django.core.exceptions.ValidationError as e:
                raise serializers.ValidationError(e.messages)
            except django.db.utils.IntegrityError as e:
                raise serializers.ValidationError(f"Такой пользователь уже существует! email: {dict_from_sheet['Почта']}")
            students.append(instance)
        return students
