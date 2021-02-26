# Project - Flask Heej
> 개인 프로젝트입니다.
- 서버개발 1년, 그동안의 경험을 한데 **모으고 확장**해 나가기 위함.
- 경험하지 못한 **기술스택**이나 시도하지 못했던 **아키텍처** 등을 하나씩 도입.
- 서비스 형태는 **SNS** 이나 향후 다양한 기능과 형태로 변화해 나갈것.

# Environment
- [`python : 3.6.6`](https://www.python.org/downloads/release/python-366/)
- [`Flask : 1.1.2`](https://flask.palletsprojects.com/en/1.1.x/)
- [`Mysql : 5.7.32`](https://www.mysql.com/)
- [`Jinja2 : 2.11.3`](https://jinja.palletsprojects.com/en/2.11.x/)
- [`bootstrap`](https://jinja.palletsprojects.com/en/2.11.x/)


# Usage
1. 환경변수 파일 작성 ``` .env```
    <details>
    <summary>환경변수 목록</summary>

    * FLASK_CONFIG
    * DEV_DATABASE_URL
    * TEST_DATABASE_URL
    * DATABASE_URL
    * MAIL_USERNAME
    * MAIL_PASSWORD
    * MAIL_SERVER
    * MAIL_PORT
    * ADMINS
    * SECRET_KEY

    </details>
2. 가상환경 생성 ```python3 -m venv env```
3. 파이썬 모듈 설치 ```pip install -r requirements.txt```
4. 데이터베이스 스키마 생성
5. 실행 스크립트 실행 ```bash run.sh```