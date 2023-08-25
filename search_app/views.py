from django_elasticsearch_dsl_drf.filter_backends import (
    CompoundSearchFilterBackend,
    NestedFilteringFilterBackend,
    SimpleQueryStringSearchFilterBackend
)
from django_elasticsearch_dsl_drf.constants import (
        LOOKUP_FILTER_TERM,
        LOOKUP_FILTER_PREFIX,
        LOOKUP_FILTER_WILDCARD,
        LOOKUP_QUERY_EXCLUDE,
        LOOKUP_QUERY_ISNULL,
        LOOKUP_FILTER_TERMS
    )
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from .documents import ProjectDocument
from .serializers import ProjectDocumentSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from elasticsearch_dsl import Q


class ProjectSearchViewSet(DocumentViewSet):
    document = ProjectDocument
    serializer_class = ProjectDocumentSerializer
    filter_backends = [CompoundSearchFilterBackend, NestedFilteringFilterBackend]
    search_fields = {
        "users": None,
    }

    filter_fields = {
        "users": "users.id.raw",
    }
    nested_filter_fields = {
        'users': {
            'field': ['users.id'],
            'path': 'users',
            'lookups': [
                LOOKUP_FILTER_TERM,
                LOOKUP_FILTER_TERMS,
                LOOKUP_FILTER_PREFIX,
                LOOKUP_FILTER_WILDCARD,
                LOOKUP_QUERY_EXCLUDE,
                LOOKUP_QUERY_ISNULL,
            ],
        },


    }
    search_nested_fields = {
        'users': {
            'fields': ['id'],
            'path': 'users',
        },
    }


class ProjectHashtagSearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get("query", "")

        # Search in the Elasticsearch index
        search = ProjectDocument.search()

        # Apply search filters and queries
        search = search.query(
            Q("nested", path="hashtags", query=Q("match", **{"hashtags.name": query}))
        )

        response = search.execute()

        projects = [hit for hit in response]
        project_serializer = ProjectDocumentSerializer(projects, many=True)

        return Response(project_serializer.data, status=status.HTTP_200_OK)


class ProjectFuzzySearchViewSet(DocumentViewSet):
    document = ProjectDocument
    serializer_class = ProjectDocumentSerializer
    filter_backends = [CompoundSearchFilterBackend]
    search_fields = {
        "slug": {'fuzziness': 'AUTO'},
        "description": {'fuzziness': 'AUTO'},
    }


