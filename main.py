from config import Config

from flask import Flask, request,jsonify
from flask_restful import Resource, Api,reqparse
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy import update,delete
from sqlalchemy.sql import insert,and_
from pprint import pprint
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import JWTManager,jwt_required,get_jwt_identity
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from schemas import VideoSchema,UserSchema,AuthSchema
from flask_apispec import use_kwargs,marshal_with
import logging

engine = create_engine('mysql+pymysql://root:1@localhost:27017/api', echo=True)
session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base = declarative_base()
Base.query = session.query_property()
Base.metadata.create_all(bind=engine)


def setup_logger():
	logger = logging.getLogger(__name__)
	logger.setLevel('DEBUG')
	formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s:%(lineno)s')
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
docs.init_app(app)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='videoblog',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
})


# Base = automap_base()
# Base.prepare(engine,reflect=True)
# Avto = Base.classes.avto
# Cities = Base.classes.cities
# Session = sessionmaker(bind = engine )
# session = Session()
# Base = 
# conn = engine.connect()
# dbresult = session.query(Avto).filter(Avto.price < 200000).all()
# result = []
# for i in dbresult:
	# result.append({
			# 'name':i.name,
			# 'price':i.price,
			# 'year':i.year})


@app.route('/tutorials',methods=['GET'],endpoint='get_list')
@jwt_required()
@marshal_with(VideoSchema(many=True))
def get_list():
	try:

		from models import Video

		user_id = get_jwt_identity()
		videos = Video.get_user_list(user_id=user_id)
	except Exception as e:
		user_id = get_jwt_identity()
		logger.warning(f'user:{user_id} tutorials - read action filed with error: {e}')
		return {'message':str(e)}, 400
	return videos



@app.route('/tutorials',methods=['POST'],endpoint='update_list')
@jwt_required()
@use_kwargs(VideoSchema)
@marshal_with(VideoSchema)
def update_list(**kwargs):
	try:
		from models import Video

		user_id = get_jwt_identity()
		new_one = Video(user_id=user_id,**kwargs)
		new_one.save()
	except Exception as e:
		logger.warning(f'user:{user_id} tutorials - create action filed with error: {e}')
		return {'message':str(e)}, 400

	return new_one	

@app.route('/tutorials/<int:tutorials_id>',methods=['PUT'],endpoint='update_tutorials')
@jwt_required()
@use_kwargs(VideoSchema)
@marshal_with(VideoSchema)
def update_tutorials(tutorials_id,**kwargs):
	try:
		from models import Video
	
		user_id = get_jwt_identity()
		# item = Video.get(tutorials_id,user_id)
		# item.update(**kwargs)
		item = Video.update(tutorials_id,user_id,kwargs)

		# stmt = update(Video).where(and_(Video.id == tutorials_id,Video.user_id==user_id)).values(**kwargs)
		# session.execute(stmt)
		# session.commit()
		# item = session.execute(""" select * from videos where id='{id_}' """.format(id_ = tutorials_id)).first()
	except Exception as e:
		logger.warning(f'user:{user_id},tutorial_id:{tutorials_id} tutorials - update action filed with error: {e}')

		return {'message':str(e)}, 400

	return item,200

@app.route('/tutorials/<int:tutorials_id>',methods=['DELETE'],endpoint='delete_tutorials')
@jwt_required()
@marshal_with(VideoSchema)
def delete_tutorials(tutorials_id):
	try:
		from models import Video

		user_id = get_jwt_identity()
		item = Video.get(tutorials_id,user_id)
		item.delete()
		# item = Video.query.filter(Video.id == tutorials_id,Video.user_id==user_id).first()
		# params = request.json
		# stmt = delete(Video).where(and_(Video.id == tutorials_id,Video.user_id==user_id))
		# session.execute(stmt)
		# session.commit()
	except Exception as e:
		logger.warning(f'user:{user_id},tutorial_id:{tutorials_id} tutorials - delete action filed with error: {e}')

		return {'message':str(e)}, 400
	return 204


@app.route('/register',methods=['POST'],endpoint='register')
@use_kwargs(UserSchema)
@marshal_with(AuthSchema)
def register(**kwargs):
	try:
		from models import Video,User

		user = User(**kwargs)
		session.add(user)
		session.commit()
		token = user.get_token()
	except Exception as e:
		logger.warning(f'Register with email:{kwargs["email"]} files with error: {e}')

		return {'message':str(e)}, 400
	return {'access_token':token}


@app.route('/login',methods=['POST'],endpoint='login')
@use_kwargs(UserSchema(only=('email','password')))
@marshal_with(AuthSchema)
def login(**kwargs):
	try:
		from models import Video,User
		user = User.authenticate(**kwargs)
		token = user.get_token()
		return {'access_token':token,'user_id':user.id}
	except Exception as e:
		logger.warning(f'Login with email:{kwargs["email"]} files with error: {e}')

		return {'message':str(e)}, 400


@app.errorhandler(422)
def error_handler(err):
	headers = err.data.get('headers',None)
	message = err.data.get('message',['Invalid request'])
	logger.warning(f'Invalid input params:{message}')

	if headers:
		return jsonify({'message':message}), 400 ,headers
	else:
		return jsonify({'message':message}), 400 ,headers




docs.register(update_list)
docs.register(get_list)
docs.register(update_tutorials)
docs.register(delete_tutorials)
docs.register(login)
docs.register(register)


if __name__ == '__main__':
	app.run(debug=True)