from flask import Blueprint,jsonify
from videoblog import logger,docs
from videoblog.schemas import VideoSchema,UserSchema,AuthSchema
from flask_apispec import use_kwargs,marshal_with
from flask_jwt_extended import JWTManager,jwt_required,get_jwt_identity
from videoblog.base_view import BaseView
from videoblog.models import Video


vids = Blueprint('vids',__name__)


class ListView(BaseView):
	@marshal_with(VideoSchema(many=True))
	def get(self):
		try:
			videos = Video.get_list()
		except Exception as e:
			logger.warning(f' tutorials - read action filed with error: {e}')
			return {'message':str(e)}, 400
		return videos




@vids.route('/tutorials',methods=['GET'],endpoint='get_list')
@jwt_required()
@marshal_with(VideoSchema(many=True))
def get_list():
	try:


		user_id = get_jwt_identity()
		videos = Video.get_user_list(user_id=user_id)
	except Exception as e:
		user_id = get_jwt_identity()
		logger.warning(f'user:{user_id} tutorials - read action filed with error: {e}')
		return {'message':str(e)}, 400
	return videos



@vids.route('/tutorials',methods=['POST'],endpoint='update_list')
@jwt_required()
@use_kwargs(VideoSchema)
@marshal_with(VideoSchema)
def update_list(**kwargs):
	try:

		user_id = get_jwt_identity()
		new_one = Video(user_id=user_id,**kwargs)
		new_one.save()
	except Exception as e:
		logger.warning(f'user:{user_id} tutorials - create action filed with error: {e}')
		return {'message':str(e)}, 400

	return new_one	

@vids.route('/tutorials/<int:tutorials_id>',methods=['PUT'],endpoint='update_tutorials')
@jwt_required()
@use_kwargs(VideoSchema)
@marshal_with(VideoSchema)
def update_tutorials(tutorials_id,**kwargs):
	try:
	
		user_id = get_jwt_identity()
		item = Video.update(tutorials_id,user_id,kwargs)

	except Exception as e:
		logger.warning(f'user:{user_id},tutorial_id:{tutorials_id} tutorials - update action filed with error: {e}')

		return {'message':str(e)}, 400

	return item,200

@vids.route('/tutorials/<int:tutorials_id>',methods=['DELETE'],endpoint='delete_tutorials')
@jwt_required()
@marshal_with(VideoSchema)
def delete_tutorials(tutorials_id):
	try:

		user_id = get_jwt_identity()
		item = Video.get(tutorials_id,user_id)
		item.delete()
	except Exception as e:
		logger.warning(f'user:{user_id},tutorial_id:{tutorials_id} tutorials - delete action filed with error: {e}')

		return {'message':str(e)}, 400
	return 204


@vids.errorhandler(422)
def error_handler(err):
	headers = err.data.get('headers',None)
	message = err.data.get('message',['Invalid request'])
	logger.warning(f'Invalid input params:{message}')

	if headers:
		return jsonify({'message':message}), 400 ,headers
	else:
		return jsonify({'message':message}), 400 ,headers


docs.register(update_list,blueprint='vids')
docs.register(get_list,blueprint='vids')
docs.register(update_tutorials,blueprint='vids')
docs.register(delete_tutorials,blueprint='vids')
ListView.register(vids,docs,'/main','listview')
