# ch03 Django 이미지 블로그 + REST API

예비 코드(https://github.com/kiokahn/web_blog)를 바탕으로 ch03 실습 전체를 진행한 코드입니다.

## ch03 실습 내용

| 실습 | 파일 |
|---|---|
| 모델에 이미지 필드 추가 (`ImageField`, Pillow) | `blog/models.py`, `blog/migrations/0002_post_image.py` |
| 미디어 경로 설정, static/media URL 패턴 | `mysite/settings.py`, `mysite/urls.py` |
| 템플릿에 이미지 출력 (`<img src="{{ post.image.url }}">`) | `blog/templates/blog/post_list.html`, `post_detail.html` |
| CSS 이미지 형식 (`.blog-image-list`) | `blog/static/css/blog.css` |
| 웹 폼으로 이미지 업로드 (`request.FILES`, `enctype="multipart/form-data"`) | `blog/forms.py`, `blog/views.py`, `post_edit.html` |
| Django REST framework: Serializer / ViewSet / Router | `blog/serializers.py`, `blog/views.py`(`blogImage`), `blog/urls.py` |
| 토큰 인증 (`rest_framework.authtoken`, `/api-token-auth/`) | `mysite/settings.py`, `mysite/urls.py`, `blog/authentication.py` |
| Python 코드를 이용한 API 테스트 | `test_api/test_api.py` |

- API 조회(GET)는 누구나, 작성(POST)/수정/삭제는 인증된 사용자만 가능 (`IsAuthenticatedOrReadOnly`).
- 강의 자료의 curl 예제처럼 `Authorization: JWT <token>` 헤더로 토큰 인증이 되도록
  `blog/authentication.py` 에서 DRF `TokenAuthentication` 의 keyword 를 `JWT` 로 지정했습니다.

## 실행 방법

```bash
cd ch03_web_blog
python3 -m venv ./venv
source ./venv/bin/activate          # Windows: .\venv\Scripts\activate
pip install -r requirements.txt     # Django 6.1.1 → Python 3.12 이상 필요
python manage.py migrate
python manage.py createsuperuser
python manage.py drf_create_token <username>   # API 토큰 발급
python manage.py runserver
```

- 사용자: http://127.0.0.1:8000/
- 관리자: http://127.0.0.1:8000/admin/
- API Root: http://127.0.0.1:8000/api_root/ , 게시물 API: http://127.0.0.1:8000/api_root/Post/

## API 테스트

### curl (ID/Password)
```bash
curl -X POST -S -H 'Accept: application/json' -u "username:password" \
  -F "author=1" -F "title=제목" -F "text=API 내용" \
  -F "created_date=2026-09-28T18:34:00+09:00" -F "published_date=2026-09-28T18:34:00+09:00" \
  -F "image=@test_api/figure.jpg;type=image/jpg" \
  http://127.0.0.1:8000/api_root/Post/
```

### curl (토큰)
```bash
curl -X POST -S -H "Authorization: JWT <token>" -H 'Accept: application/json' \
  -F "author=1" -F "title=curl 테스트" -F "text=API curl로 작성된 AP 테스트 입력 입니다." \
  -F "created_date=2026-09-28T18:34:00+09:00" -F "published_date=2026-09-28T18:34:00+09:00" \
  -F "image=@test_api/figure.jpg;type=image/jpg" \
  http://127.0.0.1:8000/api_root/Post/
```

### Python (requests)
```bash
pip install requests
API_USER=<username> API_PASSWORD=<password> python test_api/test_api.py
```

## PythonAnywhere 배포 (요약)

```bash
git clone https://github.com/vyjsjs/Django-blog.git
cd Django-blog/ch03_web_blog
python3.13 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate && python manage.py collectstatic --noinput
python manage.py createsuperuser
```
Web 탭: Manual configuration / Python 3.13, Virtualenv `~/Django-blog/ch03_web_blog/venv`,
Static files `/static/` → `.../ch03_web_blog/staticfiles`, `/media/` → `.../ch03_web_blog/media`,
WSGI 파일의 `path` 를 `/home/<username>/Django-blog/ch03_web_blog` 로, `DJANGO_SETTINGS_MODULE=mysite.settings`.
