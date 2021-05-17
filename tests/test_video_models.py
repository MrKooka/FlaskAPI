


def test_list(video,client,user_headers):
	res = client.get('/tutorials',headers = user_headers)

	assert res.status_code == 200
	assert len(res.get_json())== 0

	assert res.get_json()[0]
def test_new_video(user,client,user_headers):
	res = client.post('/tutorials',json={
		'desc':'Описание',
		'name':'Видео 1'
		}, headers=user_headers)

	assert res.status_code == 200
	assert res.get_json()['name'] == 'Видео 1'
	assert res.get_json()['desc'] == 'Описание'
	assert res.get_json()['user_id'] == user.id

def test_edit_video(video,client,user_headers):
	res = client.put(
		f'/tutorials/{video.id}',
		json={'name':'Edit name','desc':'edit desc'},
		headers=user_headers
	)
	assert res.status_code == 200
	assert res.get_json()['name'] == 'Edit name'
	assert res.get_json()['desc'] == 'edit desc'

def test_delete_video(video,client,user_headers):
	res = client.delete(
		f'/tutorials/{video.id}',
		headers=user_headers,)
	assert res.status_code == 204