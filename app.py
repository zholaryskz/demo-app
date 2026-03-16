from flask import Flask, jsonify
import os
import psycopg2
app = Flask(__name__)
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "pass123")
@app.get("/")
def index():
    return jsonify(message="Demo app is running")
@app.get("/health")
def health():
    return jsonify(status="ok")
@app.get("/db-check")
def db_check():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=3
        )
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        result = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify(db="ok", result=result)
    except Exception as e:
        return jsonify(db="error", details=str(e)), 500
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
