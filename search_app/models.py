from django.db import models


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class Hashtags(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class Projects(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hashtags = models.ManyToManyField(Hashtags, through='ProjectHashtags', related_name='projects')
    users = models.ManyToManyField(Users, through='UserProjects', related_name='projects')


class ProjectHashtags(models.Model):
    hashtag = models.ForeignKey(Hashtags, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)


class UserProjects(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
