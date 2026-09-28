# ch03-02 Python 소켓 서버 (HTTP Request 확인)

클라이언트(curl)가 보낸 HTTP 요청을 소켓 수준에서 받아 확인하는 서버입니다.

- **실습 1**: 클라이언트 요청을 그대로 `request/년-월-일-시-분-초.bin` 이진 파일로 저장
- **실습 2**: `multipart/form-data` 본문을 boundary 로 분리해, 이미지 파트를
  `request/년-월-일-시-분-초_<원본파일명>` 으로 저장

## 파일

| 파일 | 설명 |
|---|---|
| `socket_server.py` | 소켓 서버 (포트 8000) |
| `response.bin` | 클라이언트에게 보내는 고정 HTTP 응답 |
| `figure.jpg` | curl 로 전송한 테스트 이미지 |
| `request/2026-09-28-21-56-20.bin` | **출력 1** - 수신한 요청 원본 (헤더 + 멀티파트 본문) |
| `request/2026-09-28-21-56-20_figure.jpg` | **출력 2** - 멀티파트에서 추출한 이미지 (원본 `figure.jpg` 와 바이트 단위로 동일) |
| `server_log.txt` | 위 요청을 처리할 때의 서버 출력 |

## 구현 요점

1. 헤더 끝(`\r\n\r\n`)까지 수신 → `Content-Length` 만큼 본문을 추가 수신
   (`bufsize=1024` 로 여러 번 `recv` 해야 이미지 전체를 받을 수 있음)
2. curl 은 1MB 이상 전송 시 `Expect: 100-continue` 를 보내고 기다리므로 `HTTP/1.1 100 Continue` 를 먼저 응답
3. `Content-Type` 헤더의 `boundary` 로 본문을 나누고, 각 파트의 `Content-Disposition`(name, filename)과
   `Content-Type` 을 확인해 `image/*` 파트만 파일로 저장. 텍스트 필드는 콘솔에 출력

## 실행

```bash
# 터미널 1
python3 socket_server.py

# 터미널 2 (과제의 curl 명령, 이미지 경로만 변경)
curl -X POST -S -H "Authorization: JWT b181ce4155b7413ebd1d86f1379151a7e035f8bd" -F "author=1" \
  -H 'Accept: application/json' -F "title=curl 테스트" -F "text=API curl로 작성된 AP 테스트 입력 입니다." \
  -F "created_date=2024-06-10T18:34:00+09:00" -F "published_date=2024-06-10T18:34:00+09:00" \
  -F "image=@./figure.jpg;type=image/jpg" http://127.0.0.1:8000/api_root/Post/
```

> Django 서버와 같은 8000 포트를 쓰므로 Django `runserver` 는 꺼둔 상태에서 실행합니다.
