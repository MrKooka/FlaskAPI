

def test_model(user):
	assert user.name == 'Testuser'

def test_user_login(user,client):
	res = client.post('/login',json={
			'email':user.email,
			'password':'password'})
	assert res.status_code == 200
	assert res.get_json().get('access_token')

def test_user_teg(client):
	res =client.post('/register',json={
	 	"email":"test@test.test",
	 	"name":"Testuser",
	 	"password":"password"})
	assert res.status_code == 200
	assert res.get_json().get('access_token')

