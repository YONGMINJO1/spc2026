import os
import sqlite3
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                likes INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Insert a sample welcoming post so the board isn't completely empty initially
        conn.execute('''
            INSERT INTO posts (title, message, likes) 
            VALUES (?, ?, ?)
        ''', ('Welcome to Board Vibe! ✨', 'Feel free to leave your vibrant thoughts here. Enjoy the premium micro-interactions and dark neon mood!', 5))
        conn.commit()
        conn.close()

# Initialize Database
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/posts', methods=['GET'])
def get_posts():
    try:
        conn = get_db_connection()
        posts = conn.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()
        conn.close()
        
        post_list = []
        for post in posts:
            post_list.append({
                'id': post['id'],
                'title': post['title'],
                'message': post['message'],
                'likes': post['likes'],
                'created_at': post['created_at']
            })
        return jsonify(post_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts', methods=['POST'])
def create_post():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid payload'}), 400
            
        title = data.get('title', '').strip()
        message = data.get('message', '').strip()
        
        if not title or not message:
            return jsonify({'error': 'Title and Message are required'}), 400
            
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO posts (title, message) VALUES (?, ?)',
            (title, message)
        )
        conn.commit()
        new_id = cursor.lastrowid
        
        # Fetch the newly created post to return it
        new_post = conn.execute('SELECT * FROM posts WHERE id = ?', (new_id,)).fetchone()
        conn.close()
        
        return jsonify({
            'id': new_post['id'],
            'title': new_post['title'],
            'message': new_post['message'],
            'likes': new_post['likes'],
            'created_at': new_post['created_at']
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    try:
        conn = get_db_connection()
        post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
        if not post:
            conn.close()
            return jsonify({'error': 'Post not found'}), 404
            
        conn.execute('UPDATE posts SET likes = likes + 1 WHERE id = ?', (post_id,))
        conn.commit()
        
        updated_post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
        conn.close()
        
        return jsonify({
            'id': updated_post['id'],
            'likes': updated_post['likes']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        conn = get_db_connection()
        post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
        if not post:
            conn.close()
            return jsonify({'error': 'Post not found'}), 404
            
        conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Post deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
