import os
class Config:
	 # SECRET_KEY = '4d10b3dd8c3c431a88f5ad707e1be440'
	 SECRET_KEY = os.environ.get('SECRET_KEY')