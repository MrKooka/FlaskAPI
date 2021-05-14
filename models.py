from main import db,session,Base,engine
from sqlalchemy.orm import relationship
from flask_jwt_extended import create_access_token
from datetime import timedelta
from passlib.hash import bcrypt
class Video(Base):
	__tablename__ = 'videos'
	id = db.Column(db.Integer,primary_key=True)
	user_id = db.Column(db.Integer,db.ForeignKey('userapi.id'))
	name = db.Column(db.String(225),nullable=False)
	desc = db.Column(db.String(500),nullable=False)


class User(Base):
	__tablename__='userapi'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(225),nullable=False)
	email = db.Column(db.String(225),nullable=False,unique=True)
	password = db.Column(db.String(100),nullable=False)
	videos = relationship('Video',backref='user',lazy =True)

	def __init__(self,**kwargs):
		self.name = kwargs.get('name')
		self.email = kwargs.get('email')
		self.password = bcrypt.hash(kwargs.get('password'))

	def get_token(self,expire_tieme=24):
		expire_delta = timedelta(expire_tieme)
		token = create_access_token(identity= self.id,expires_delta=expire_delta)
		return token

	@classmethod 
	def authenticate(cls,email,password):
		user = cls.query.filter(cls.email==email).one()
		if not bcrypt.verify(password,user.password):
			raise Exception('No user with this password')
		return user

