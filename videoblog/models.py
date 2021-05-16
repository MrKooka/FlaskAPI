from . import db,session,Base,engine
from sqlalchemy.orm import relationship
from flask_jwt_extended import create_access_token
from datetime import timedelta
from passlib.hash import bcrypt
from sqlalchemy import update,delete
from sqlalchemy.sql import insert,and_,select

class Video(Base):
	__tablename__ = 'videos'
	id = db.Column(db.Integer,primary_key=True)
	user_id = db.Column(db.Integer,db.ForeignKey('userapi.id'))
	name = db.Column(db.String(225),nullable=False)
	desc = db.Column(db.String(500),nullable=False)

	@classmethod
	def get_user_list(cls,user_id):
		try:
			videos = cls.query.filter(cls.user_id == user_id).all()
			session.commit()
		except Exception:
			session.rollback()
			raise
		return videos

	@classmethod
	def get_list(cls):
		try:
			videos = cls.query.all()
			session.commit()
		except Exception:
			session.rollback()
			raise
		return videos


	def save(self):
		try:
			session.add(self)
			session.commit()
		except Exception:
			session.rollback()
			raise

	@classmethod
	def get(cls,tutorial_id,user_id):
		try:
			video = cls.query.filter(cls.id == tutorial_id,cls.user_id==user_id).first()
			if not video:
				raise Exception('No tutorials with this id')

		except Exception:
			session.rollback()
			raise
		return video
		
	@classmethod
	def update(cls,tutorials_id,user_id,kwargs):
		try:
			stmt = update(cls).where(and_(cls.id == tutorials_id,cls.user_id==user_id)).values(**kwargs)
			session.execute(stmt)
			session.commit()
			item = cls.query.filter(cls.id == tutorials_id).first()

		except Exception:
			session.rollback()
			raise
		return item

	def delete(self):
		try:
			session.delete(self)
			session.commit()
		except Exception:
			session.rollback()
			raise

	



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

