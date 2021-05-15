from . import client
from models import *
def test_simple():
	mylist = [1,2,3,4,5,6]
	assert 2 in mylist

def test_get_1():
	res = client.get('/tutorials')
	assert res.status_code == 200
	assert res.get_json()[0]['id'] == 4

def test_post():
	data = {
		'name':'video 3',
		'desc':'dsc of title 3 '
	}
	res = client.post('/tutorials',json=data)
	assert res.status_code == 200

def test_put():
	res = client.put('/tutorials/3',json={'name':'UPD'})
	assert res.status_code == 200
	assert Video.query.get(3).name in 'UPD'


def test_delete():
	res = client.delete('/tutorials/3')

	assert res.status_code == 204
	assert Video.query.get(3) is None
