from flask import Blueprint,jsonify
from videoblog import logger,docs
from videoblog.schemas import UserSchema,AuthSchema
from flask_apispec import use_kwargs,marshal_with

users = Blueprint('users',__name__)

@users.route('/register',methods=['POST'],endpoint='register')
@use_kwargs(UserSchema)
@marshal_with(AuthSchema)
def register(**kwargs):
	try:
		from videoblog.models import User

		user = User(**kwargs)
		session.add(user)
		session.commit()
		token = user.get_token()
	except Exception as e:
		logger.warning(f'Register with email:{kwargs["email"]} files with error: {e}')

		return {'message':str(e)}, 400
	return {'access_token':token}


@users.route('/login',methods=['POST'],endpoint='login')
@use_kwargs(UserSchema(only=('email','password')))
@marshal_with(AuthSchema)
def login(**kwargs):
	try:
		from videoblog.models import User
		user = User.authenticate(**kwargs)
		token = user.get_token()
		return {'access_token':token,'user_id':user.id}
	except Exception as e:
		logger.warning(f'Login with email:{kwargs["email"]} files with error: {e}')

		return {'message':str(e)}, 400

@users.errorhandler(422)
def error_handler(err):
	headers = err.data.get('headers',None)
	message = err.data.get('message',['Invalid request'])
	logger.warning(f'Invalid input params:{message}')

	if headers:
		return jsonify({'message':message}), 400 ,headers
	else:
		return jsonify({'message':message}), 400 ,headers


docs.register(login,blueprint='users')
docs.register(register,blueprint='users')


