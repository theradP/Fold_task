from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Users, Projects, Hashtags
from .documents import ProjectsDocument
from .serializers import ProjectSerializer


class ProjectSearchViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test data
        self.user = Users.objects.create(name="Test User")
        self.hashtag1 = Hashtags.objects.create(name="Tag1")
        self.hashtag2 = Hashtags.objects.create(name="Tag2")
        self.project = Projects.objects.create(
            name="Test Project",
            slug="test-project",
            description="Test description",
        )

        self.project.hashtags.add(self.hashtag1, self.hashtag2)
        self.project.refresh_from_db()

        ProjectsDocument().update()

    def test_search_by_project_name(self):
        response = self.client.get(reverse("project-search-list"), {"search": "Test"})
        projects = Projects.objects.filter(name__icontains="Test")
        serializer = ProjectSerializer(projects, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_search_by_hashtag(self):
        response = self.client.get(reverse("project-search-list"), {"search": "Tag1"})
        projects = Projects.objects.filter(hashtags__name__icontains="Tag1")
        serializer = ProjectSerializer(projects, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_search_by_user_id(self):
        response = self.client.get(
            reverse("project-search-list"), {"user_id": self.user.id}
        )
        projects = Projects.objects.filter(user__id=self.user.id)
        serializer = ProjectSerializer(projects, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_search_by_user_name(self):
        response = self.client.get(
            reverse("project-search-list"), {"user_name": self.user.name}
        )
        projects = Projects.objects.filter(user__name__icontains=self.user.name)
        serializer = ProjectSerializer(projects, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
