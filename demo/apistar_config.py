import logging
import time
import datetime
import bcrypt
from apistar_jwt import JWT, JWTUser, anonymous_allowed
from apistar import types, validators, exceptions, App
from apistar import Route
from apistar_jwt import anonymous_allowed, JWT

from .database import DbWrapper

log = logging.getLogger(__name__)


JWT_EXPIRATION_TIME = datetime.timedelta(hours=1)


@anonymous_allowed
def hello_world():
    return {"message": "Welcome to Omnisyan!"}


class UserData(types.Type):
    """ You must supply either email or phone, plus the password. """
    email = validators.String(description="Email address for authentication.", pattern="[^@]+@[^@]+\.[^@]+", allow_null=True)
    phone = validators.String(description="Or phone number for authentication.", pattern="\D*", allow_null=True)
    password = validators.String()

    def __init__(self, *args, **kwargs):
        """ additional validation rules """
        super().__init__(*args, **kwargs)
        if not self.email and not self.phone:
            raise exceptions.ValidationError('You must supply one of Email or Phone.')


class AuthenticatedUserData(types.Type):
    id = validators.Integer()
    email = validators.String(description="Email address", pattern="[^@]+@[^@]+\.[^@]+", allow_null=True)
    phone = validators.String(description="Phone number", pattern="\D*", allow_null=True)
    first_name = validators.String()
    last_name = validators.String()
    language = validators.Integer()
    groups = validators.Array()
    location = validators.Integer()
    picture = validators.String(allow_null=True)


def db_login(data: UserData) -> AuthenticatedUserData:
    db = DbWrapper()
    db.cursor.execute(
        """SELECT 
            id, 
            firstname as first_name, 
            surname as last_name, 
            email, 
            phone, 
            userlanguage as language, 
            password, 
            groupid as groups,
            locationid as location,
            picture
        FROM backoffice.users 
        WHERE 
          not del 
          and (
            email = %(email)s
            OR phone = %(phone)s
          )
        LIMIT 1""",
        data
    )
    result = db.cursor.fetchone()
    if not result or not bcrypt.checkpw(data.password.encode('utf8'), result['password'].encode('utf8')):
        raise exceptions.Forbidden("Invalid login credentials.")
    return AuthenticatedUserData(dict(result))


@anonymous_allowed
def login(data: UserData, jwt: JWT) -> dict:
    # do some check with your database here to see if the user is authenticated
    user = db_login(data)
    # print(user)
    if not user:
        raise exceptions.Forbidden('Incorrect username or password.')
    payload = {
        'id': user.id,
        'username': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': user.phone,
        'language': user.language,
        'groups': user.groups,
        'location': user.location,
        'picture': user.picture,
        # expiration data
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + JWT_EXPIRATION_TIME
    }
    # noinspection PyUnresolvedReferences
    token = jwt.encode(payload)
    if token is None:
        # encoding failed, handle error
        raise exceptions.BadRequest()
    return {'token': token}


def welcome(user: JWTUser) -> dict:
    time_left = user.token["exp"] - time.mktime(datetime.datetime.now().timetuple())
    message = f'''
        Welcome {user.username}#{user.id}, 
        your login expires at {user.token["exp"]} 
        ({time_left} seconds remaining.) 
    '''
    return {'message': message}


def whoami(user: JWTUser) -> dict:
    time_left = user.token["exp"] - time.mktime(datetime.datetime.now().timetuple())
    # print(type(user), user)
    location = {}
    try:
        sql = """SELECT name, centroid FROM reference.locations WHERE id = %(location)s and not del"""
        db = DbWrapper()
        db.cursor.execute(sql, user.token)
        result = db.cursor.fetchone()
        if result:
            location = dict(result)
    except Exception as e:
        log.exception(e)
    return {
        'user': dict(user.__dict__),
        'location': location,
        'login_time_remaining': time_left,
    }


routes = [
    Route('/', method='GET', handler=hello_world),
    Route('/login', method='POST', handler=login),
    Route('/test', method='GET', handler=welcome),
    Route('/whoami', method='GET', handler=whoami),
]

components = [
    JWT({'JWT_SECRET': "shhhh-dont-tell-anyone",
         })
]


class ApistarApp(App):
    pass
