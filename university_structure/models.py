from django.db import models


class Group(models.Model):
    name = models.CharField(unique=True, max_length=256)
    department = models.ForeignKey("Department", on_delete=models.CASCADE, related_name='groups', null=True)


class Department(models.Model):
    name = models.CharField(unique=True, max_length=256)
    faculty = models.ForeignKey("Faculty", on_delete=models.CASCADE, related_name="departments")


class Faculty(models.Model):
    name = models.CharField(unique=True, max_length=256)


class News(models.Model):

    title = models.CharField(unique=True, max_length=256)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey("users.UserETU", on_delete=models.CASCADE, related_name="news")
    faculty = models.ForeignKey("Faculty", on_delete=models.CASCADE, related_name="news")
    coin_reward = models.PositiveIntegerField(default=0, verbose_name="Награда за выполнение")
    image = models.ImageField(upload_to='news_images/', null=True, verbose_name="Изображение")



