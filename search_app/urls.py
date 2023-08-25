from rest_framework.routers import DefaultRouter
from .views import ProjectSearchViewSet, ProjectHashtagSearchAPIView, ProjectFuzzySearchViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r"projects/user", ProjectSearchViewSet, basename="project-search-user")
router.register(r"projects/fuzzy", ProjectFuzzySearchViewSet, basename="project-search-fuzzy")
urlpatterns = [
    # Other URLs
    path("projects/hashtag-search/", ProjectHashtagSearchAPIView.as_view(), name="project-hashtag-search"),
]
urlpatterns += router.urls