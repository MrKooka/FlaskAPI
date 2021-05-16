


def test_list(video,client,user_headers):
	res = client.get('/tutorials',headers = user_headers)

	assert res.status_code == 200
	assert len(res.get_json())== 0

	assert res.get_json()[0]