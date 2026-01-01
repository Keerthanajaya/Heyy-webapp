from flask import Flask, render_template, request, jsonify
from datetime import datetime
from database import init_db, get_db_connection

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    nickname = data.get('nickname', 'Anonymous')
    message = data.get('message', '')
    timestamp = datetime.now().strftime('%H:%M:%S')

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO messages (nickname, message, time) VALUES (?, ?, ?)",
        (nickname, message, timestamp)
    )
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

@app.route('/get_messages', methods=['GET'])
def get_messages():
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT nickname, message, time FROM messages ORDER BY id ASC"
    ).fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])
@app.route('/clear_messages', methods=['POST'])
def clear_messages():
    conn = get_db_connection()
    conn.execute("DELETE FROM messages")
    conn.commit()
    conn.close()
    return jsonify({"status": "cleared"})


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
