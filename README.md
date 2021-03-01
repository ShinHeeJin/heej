# Project - Flask Heej
> 개인 프로젝트입니다.
- 그동안의 경험을 한데 **모으고 확장**해 나가기 위함.
- 경험못한 **기술스택**, 시도하지 못했던 **아키텍처** 등을 하나씩 도입.
- 서비스 형태는 **SNS**이나, 향후 다양한 기능과 형태로 변화할 것.

# Environment
- [`python : 3.6.6`](https://www.python.org/downloads/release/python-366/)
- [`Flask : 1.1.2`](https://flask.palletsprojects.com/en/1.1.x/)
- [`Flask-SQLAlchemy 2.4.4`](https://github.com/pallets/flask-sqlalchemy)
- [`Flask-Migrate 2.7.0`](https://github.com/pallets/flask-sqlalchemy)
- [`Mysql : 5.7.32`](https://www.mysql.com/)
- [`Jinja2 : 2.11.3`](https://jinja.palletsprojects.com/en/2.11.x/)
- [`bootstrap 4.3.1`](https://getbootstrap.com/docs/4.3/getting-started/introduction/)

# Usage
1. 환경변수 파일 작성 ``` /heej/.env```
    <details>
    <summary>환경변수 목록</summary>

    * FLASK_CONFIG : 'development' or 'test' or 'production'
    * DEV_DATABASE_URL : "mysql+pymysql://username:password@host:port/mydb?charset=utf8mb4"
    * TEST_DATABASE_URL : "mysql+pymysql://username:password@host:port/mydb?charset=utf8mb4"
    * DATABASE_URL : "mysql+pymysql://username:password@host:port/mydb?charset=utf8mb4"
    * MAIL_USERNAME : 메일 송신자 계정
    * MAIL_PASSWORD : 메일 송신자 비밀번호
    * MAIL_SERVER : "smtp.gmail.com"
    * MAIL_PORT : "587"
    * ADMINS : 서비스 관리자 계정
    * SECRET_KEY : 암호화 키

    </details>
2. 가상환경 생성
    * ```python3 -m venv env```
    * ```source env/bin/activate```
3. 파이썬 모듈 설치
    * ```pip install --upgrade```
    * ```pip install -r requirements.txt```
4. 데이터베이스 스키마 생성
    * ``` mysql> CREATE DATABASE mydb ```
5. 데이터 베이스 마이그레이션
    * ``` $ export FLASK_APP=heej.py ```
    * ``` $ flask db upgrade ```