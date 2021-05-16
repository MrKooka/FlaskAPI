from flask import jsonify
from flask_apispec.views import MethodResource
from . import logger

class BaseView(MethodResource):
	@classmethod
	def register(cls,blueprint,spec,url,name):
		blueprint.add_url_rule(url,view_func = cls.as_view(name))
		blueprint.register_error_handler(422,cls.handler_erros)
		spec.register(cls,blueprint=blueprint.name)

	@staticmethod
	def handler_erros():
		headers = err.data.get('headers',None)
		message = err.data.get('message',['Invalid request'])
		logger.warning(f'Invalid input params:{message}')

		if headers:
			return jsonify({'message':message}), 400 ,headers
		else:
			return jsonify({'message':message}), 400 ,headers



