from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import pytz

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.route('/')
def index():
    # Show current Malaysia time on homepage
    malaysia_tz = pytz.timezone('Asia/Kuala_Lumpur')
    current_time = datetime.now(malaysia_tz).strftime('%Y-%m-%d %H:%M:%S MYT')
    return render_template('index.html', current_time=current_time)

@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        
        # Get current time in Malaysia timezone
        malaysia_tz = pytz.timezone('Asia/Kuala_Lumpur')
        current_time = datetime.now(malaysia_tz).strftime('%Y-%m-%d %H:%M:%S MYT')
        
        # Insert data into database
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email, age, created_at) VALUES (?, ?, ?, ?)', 
                      (name, email, age, current_time))
        conn.commit()
        conn.close()
        
        return redirect(url_for('view_data'))
    
    return render_template('add_data.html')

@app.route('/view_data')
def view_data():
    # Fetch all data from database
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users ORDER BY id ASC')
    raw_users = cursor.fetchall()
    conn.close()
    
    # Convert timestamps to Malaysia timezone for display
    malaysia_tz = pytz.timezone('Asia/Kuala_Lumpur')
    users = []
    
    for user in raw_users:
        user_list = list(user)
        # Convert timestamp (index 4) to Malaysia timezone
        if user_list[4]:  # If timestamp exists
            try:
                # Try to parse the timestamp
                if '+' in str(user_list[4]) or 'T' in str(user_list[4]):
                    # Already has timezone info or is ISO format
                    dt = datetime.fromisoformat(str(user_list[4]).replace('T', ' ').split('+')[0])
                    dt = pytz.utc.localize(dt).astimezone(malaysia_tz)
                else:
                    # Assume it's UTC and convert
                    dt = datetime.strptime(str(user_list[4]), '%Y-%m-%d %H:%M:%S')
                    dt = pytz.utc.localize(dt).astimezone(malaysia_tz)
                
                user_list[4] = dt.strftime('%Y-%m-%d %H:%M:%S MYT')
            except:
                # If conversion fails, keep original
                pass
        users.append(tuple(user_list))
    
    return render_template('view_data.html', users=users)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        # Delete the specific user
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        
        # Get all remaining users ordered by created_at to maintain chronological order
        cursor.execute('SELECT name, email, age, created_at FROM users ORDER BY created_at ASC')
        users = cursor.fetchall()
        
        # Delete all remaining records
        cursor.execute('DELETE FROM users')
        
        # Reset auto-increment counter
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="users"')
        
        # Re-insert all users with new sequential IDs
        for user in users:
            cursor.execute('INSERT INTO users (name, email, age, created_at) VALUES (?, ?, ?, ?)', user)
        
        conn.commit()
        conn.close()
        
        return redirect(url_for('view_data'))
    except Exception as e:
        return f"Error deleting user: {e}", 400



if __name__ == '__main__':
    app.run(debug=True)
