# ==============================================================================
# Imports
# ==============================================================================
from commom_imports import Flask
from commom_imports import redirect
from commom_imports import render_template
from commom_imports import request
from commom_imports import sqlite3

# Connect to the database (Or create ir)
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create table
c.execute('''
CREATE TABLE IF NOT EXISTS items (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          description TEXT NOT NULL
          )
''')

# Commit and close connection
conn.commit()
conn.close()

app = Flask(__name__)

# ==============================================================================
# Functions
# ==============================================================================
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ==============================================================================
# Routes
# ==============================================================================
# Initial route
@app.route('/')
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('index.html', items=items)

# Add new item route
@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        conn = get_db_connection()
        conn.execute('INSERT INTO items (name, description) VALUES (?, ?)', (name, description))
        conn.commit()
        conn.close()
        return redirect('/')

    return render_template('add.html')

# Edit existing item
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (id,)).fetchone()

    if item is None:
        return 'Item not found', 404

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        conn.execute('UPDATE items SET name = ?, description = ? WHERE id = ?',
                     (name, description, id))
        conn.commit()
        conn.close()
        return redirect('/')

    conn.close()
    return render_template('edit.html', item=item)

# Delete item
@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM items WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=False)