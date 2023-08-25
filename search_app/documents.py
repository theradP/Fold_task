from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Users, Hashtags, Projects, UserProjects, ProjectHashtags


@registry.register_document
class UsersDocument(Document):
    class Index:
        name = 'users'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Users
        fields = [
            'id',
            'name',
            'created_at'
        ]


@registry.register_document
class HashtagsDocument(Document):
    class Index:
        name = 'hashtags'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Hashtags
        fields = [
            'id',
            'name',
            'created_at'
        ]


@registry.register_document
class ProjectDocument(Document):
    hashtags = fields.NestedField(properties={
        'id': fields.IntegerField(attr='id'),
        'name': fields.TextField(attr='name'),
        'created_at': fields.DateField()
    })
    users = fields.NestedField(properties={
        'id': fields.IntegerField(attr='id'),
        'name': fields.TextField(attr='name'),
        'created_at': fields.DateField()
    })

    class Index:
        name = 'projects'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Projects
        fields = [
            'id',
            'slug',
            'name',
            'description',
            'created_at',
        ]
        related_models = [Hashtags, Users]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Hashtags):

            return related_instance.projects.all()
        elif isinstance(related_instance, Users):

            return related_instance.projects.all()


@registry.register_document
class ProjectUserDocument(Document):
    class Index:
        name = 'user_projects'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    project_id = fields.IntegerField(attr="project_id")
    user_id = fields.IntegerField(attr="user_id")

    class Django:
        model = UserProjects


@registry.register_document
class ProjectHashtagsDocument(Document):
    class Index:
        name = 'project_hashtags'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    project_id = fields.IntegerField(attr="project_id")
    hashtag_id = fields.IntegerField(attr="hashtag_id")

    class Django:
        model = ProjectHashtags


