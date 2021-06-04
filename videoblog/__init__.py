from .config import Config
from flask import Flask
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy.ext.automap import automap_base
from pprint import pprint
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
import logging
engine = create_engine('mysql+pymysql://root:1@localhost:27017/api', echo=True)
session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base = declarative_base()
Base.query = session.query_property()
Base.metadata.create_all(bind=engine)


def setup_logger():
	logger = logging.getLogger(__name__)
	logger.setLevel('DEBUG')
	formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(pathname)s:%(funcName)s:%(module)s:%(lineno)s:%(message)s')
	file_handler = logging.FileHandler('log/api.log')
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)

	return logger

logger = setup_logger()


app = Flask(__name__)
app.config.from_object(Config)
client = app.test_client()

# Генерация токена
jwt = JWTManager(app)

docs = FlaskApiSpec()
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='videoblog',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
})



from .main.views import vids
from .users.views import users

app.register_blueprint(vids)
app.register_blueprint(users)

docs.init_app(app)
jwt.init_app(app)







