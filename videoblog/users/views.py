from flask import Blueprint,jsonify
from videoblog import logger,docs,session
from videoblog.schemas import UserSchema,AuthSchema,VideoSchema
from flask_apispec import use_kwargs,marshal_with
from flask_jwt_extended import JWTManager,jwt_required,get_jwt_identity

from videoblog.base_view import BaseView
from videoblog.models import User

users = Blueprint('users',__name__)

@users.route('/register',methods=['POST'],endpoint='register')
@use_kwargs(UserSchema)
@marshal_with(AuthSchema)
def register(**kwargs):
	try:

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
		user = User.authenticate(**kwargs)
		token = user.get_token()
	except Exception as e:
		logger.warning(f'Login with email:{kwargs["email"]} files with error: {e}')

		return {'message':str(e)}, 400
	return {'access_token':token,'user_id':user.id}



class ProfileView(BaseView):

	@jwt_required()
	@marshal_with(UserSchema)
	def get(self):
		user_id = get_jwt_identity()
		try:
			user = User.query.get(user_id)
			if not user:
				raise Exception('User not fiund')
		except Exception as e:
			logger.warning(f'user:{user_id} filesr read profile: {e}')
		return user



docs.register(login,blueprint='users')
docs.register(register,blueprint='users')
ProfileView.register(users,docs,'/profile','profileview')


