from flask import Flask, request, render_template, redirect
import mysql.connector
from config import db_config

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert the blog post into the database
        cursor.execute("INSERT INTO blog (title, content) VALUES (%s, %s)", (title, content))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return redirect('/admin')
    
    return render_template('blog.html')

@app.route('/admin')
def admin():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM blog ")
    posts = cursor.fetchall()
    cursor.close()  
    conn.close()
    return render_template('admin.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)