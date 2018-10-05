import logging

from demo import apistar_config
from demo.apistar_config import ApistarApp
from demo.database import DbWrapper
from apistar_dynamic import ApistarDynamic

log = logging.getLogger(__name__)

FIELD_METADATA = [
    # FIELD METADATA needs to follow the rules defined by apistar https://docs.apistar.com/api-guide/type-system/
    {
        'name': 'id',
        'type': 'Integer',
        'title': None,
        'description': 'unique id',
        'attributes': {
            'allow_null': True
        }
    },
    {
        'name': 'labsubmissionid',
        'type': 'Integer',
        'title': 'Lab Submission ID',
        'description': 'System ID of the lab submission',
        'attributes': {},
    },
    {
        'name': 'animalident',
        'type': 'String',
        'title': 'animal idenity',
        'description': 'the identiy of the animal',
        'attributes': {  # suggest this is stored as a jsonb field in the database
            'max_length': 20,
        },
    },
    {
        'name': 'ownerid',
        'type': 'Integer',
        'title': 'Owner ID',
        'description': 'System ID of the owner',
        'attributes': {},
    },
    {
        'name': 'animalid',
        'type': 'Integer',
        'title': 'Animal ID',
        'description': 'System ID of the Animal',
        'attributes': {
            'allow_null': True
        },
    },
    {
        'name': 'speciesid',
        'type': 'Integer',
        'title': 'Species ID',
        'description': 'System ID of the species',
        'attributes': {},
    },
    {
        'name': 'sexid',
        'type': 'Integer',
        'title': 'sex ID',
        'description': 'System ID of the sex',
        'attributes': {
            'allow_null': True
        },
    },
    {
        'name': 'age',
        'type': 'Number',
        'title': 'animal age',
        'description': 'the age of the animal',
        'attributes': {
            'minimum': 0,
            'maximum': 100,
            'allow_null': True
        },
    },
    {
        'name': 'createdby',
        'type': 'Integer',
        'title': 'Entry Creator ID',
        'description': 'System ID of the user who created',
        'attributes': {
            'default': 1
        },
    },
    {
        'name': 'createdon',
        'type': 'String',
        'title': 'Entry Creator date',
        'description': 'date when the entry was created',
        'attributes': {
            'allow_null': True,
            'format': "datetime",
        },
    },
    {
        'name': 'modifiedby',
        'type': 'Integer',
        'title': 'Entry Creator ID',
        'description': 'System ID of the user who modified',
        'attributes': {
            'default': 1,
            'allow_null': True
        },
    },
    {
        'name': 'modifiedon',
        'type': 'String',
        'title': 'Entry Creator date',
        'description': 'date when the entry was modified',
        'attributes': {
            'allow_null': True,
            'format': "datetime"
        },
    },
    {
        'name': 'del',
        'type': 'Boolean',
        'title': 'Deleted',
        'description': 'is this entry deleted',
        'attributes': {
            'default': False
        },
    },
    {
        'name': 'ageunitsid',
        'type': 'Integer',
        'title': 'Age Units ID',
        'description': 'system id for age units reference',
        'attributes': {
            'allow_null': True
        },
    },
    {
        'name': 'msgid',
        'type': 'Integer',
        'title': 'Message ID',
        'description': 'system message id',
        'attributes': {
            'allow_null': True
        },
    },
]

# these should eventually be generated from a database
# unique 'name'
# unique together ['path', 'method']
# readonly defines if slave DB should be used.
API_METADATA = [
    {
        'name': 'add_animals',
        'data': 'Animal',
        'path': '/lab/animals/',
        'method': 'POST',
        'fields': FIELD_METADATA,
        'doc': 'Data creation handler for Animals',
        'sql': [
            '''INSERT INTO "lab"."animals" 
                  ("labsubmissionid", "animalident", "ownerid", "animalid", "speciesid", "sexid", "age", "createdby", "ageunitsid", "msgid") 
               VALUES 
                  (%(labsubmissionid)s, %(animalident)s, %(ownerid)s, %(animalid)s, %(speciesid)s, %(sexid)s, %(age)s, %(createdby)s, %(ageunitsid)s, %(msgid)s)
            ''',
        ],
        'readonly': False,
        'permission_id': 170
    },
    {
        'name': 'list_animals',
        'data': 'Animal',
        'path': '/lab/animals/',
        'method': 'GET',
        'fields': FIELD_METADATA,
        'doc': 'Animals in a laboratory submission. On submission may include several animals from several different owners',
        # 'sql': '''select id, labsubmissionid, animalident, ownerid, animalid, speciesid, sexid, age, ageunitsid, msgid
        'sql': '''select *
            from lab.animals
            where not del''',
        'readonly': True,
        'permission_id': 173

    },
    {
        'name': 'get_animal',
        'data': 'Animal',
        'path': '/lab/animals/{id}/',
        'method': 'GET',
        'fields': FIELD_METADATA,
        'doc': 'Animals in a laboratory submission. On submission may include several animals from several different owners',
        # 'sql': '''select id, labsubmissionid, animalident, ownerid, animalid, speciesid, sexid, age, ageunitsid, msgid
        'sql': '''select *
            from lab.animals
            where not del and id = %(id)s''',
        'readonly': True,
        'permission_id': 173

    },
]


class DemoApi(ApistarDynamic):
    api_metadata = API_METADATA
    database_class = DbWrapper


demo = DemoApi()

print(demo.get_dynamic_routes())

# API star settings

routes = demo.get_dynamic_routes()
routes.extend(apistar_config.routes)

app = ApistarApp(
    routes=routes,
    components=apistar_config.components
)

if __name__ == '__main__':
    app.serve('127.0.0.1', 8000, debug=True)
