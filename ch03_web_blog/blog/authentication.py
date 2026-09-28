from rest_framework.authentication import TokenAuthentication


class JWTKeywordTokenAuthentication(TokenAuthentication):
    """강의 자료의 curl 예제처럼 'Authorization: JWT <token>' 헤더를 받는 토큰 인증.

    DRF 기본 TokenAuthentication 은 'Token <token>' 형식만 인식하므로
    키워드만 'JWT' 로 바꿔서 슬라이드의 명령어가 그대로 동작하게 함.
    (실제 JWT 가 아니라 rest_framework.authtoken 의 토큰을 사용)
    """
    keyword = 'JWT'
