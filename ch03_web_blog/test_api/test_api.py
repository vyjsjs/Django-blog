"""ch03 - Python 코드를 이용한 REST API 테스트

사용법 (Django 서버가 실행 중인 상태에서):
    python test_api.py
    # 다른 서버/계정으로 테스트할 때
    HOST=https://<username>.pythonanywhere.com API_USER=admin API_PASSWORD=비밀번호 python test_api.py
"""
import os

import requests  # 오류가 있으면 "pip install requests"

HOST = os.environ.get('HOST', 'http://127.0.0.1:8000')
USERNAME = os.environ.get('API_USER', 'admin')
PASSWORD = os.environ.get('API_PASSWORD', 'password')
IMAGE_PATH = os.environ.get(
    'IMAGE_PATH', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figure.jpg'))

# 1) ID/PW 로 토큰 발급
res = requests.post(HOST + '/api-token-auth/', {
    'username': USERNAME,
    'password': PASSWORD,
})
res.raise_for_status()
token = res.json()['token']
print('token:', token)

# 인증이 필요한 요청에 아래의 headers를 붙임
headers = {'Authorization': 'JWT ' + token, 'Accept': 'application/json'}

# 2) 로그인한 사용자 id 를 author 로 사용
me = requests.get(HOST + '/api_root/Post/', headers=headers)
me.raise_for_status()

# 3) Post Create (이미지 포함, multipart/form-data)
data = {
    'author': os.environ.get('AUTHOR_ID', '1'),
    'title': '제목 by code',
    'text': 'API내용 by code (requests 라이브러리)',
    'created_date': '2026-09-28T18:34:00+09:00',
    'published_date': '2026-09-28T18:34:00+09:00',
}
with open(IMAGE_PATH, 'rb') as f:
    files = {'image': ('figure.jpg', f, 'image/jpeg')}
    res = requests.post(HOST + '/api_root/Post/', data=data, files=files, headers=headers)
print(res)
print(res.json())
res.raise_for_status()
