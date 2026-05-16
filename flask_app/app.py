import os
import socket

import psycopg2
import pymysql
import redis
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, Docker!"


def _postgres_ok():
    url = os.environ.get("DATABASE_URL")
    if not url:
        return False
    try:
        conn = psycopg2.connect(url)
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        finally:
            conn.close()
        return True
    except Exception:
        return False


def _redis_ok():
    url = os.environ.get("REDIS_URL")
    if not url:
        return False
    try:
        client = redis.from_url(url)
        return client.ping() is True
    except Exception:
        return False


def _mysql_ok():
    host = os.environ.get("MYSQL_HOST")
    user = os.environ.get("MYSQL_USER")
    password = os.environ.get("MYSQL_PASSWORD")
    database = os.environ.get("MYSQL_DATABASE")
    if not all([host, user, password, database]):
        return False
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            connect_timeout=3,
            charset="utf8mb4",
        )
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        finally:
            conn.close()
        return True
    except Exception:
        return False


@app.route("/health")
def health():
    return jsonify(
        postgres=_postgres_ok(),
        mysql=_mysql_ok(),
        redis=_redis_ok(),
        hostname=socket.gethostname(),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
