from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Conexión a la base de datos PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="APP_Tienda",
        user="postgres",
        password="********"
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM productos WHERE disponible = TRUE ORDER BY id ASC;')
    productos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', productos=productos)

@app.route('/agregar/<int:producto_id>')
def agregar(producto_id):
    if 'carrito' not in session:
        session['carrito'] = []
    session['carrito'].append(producto_id)
    session.modified = True
    return redirect(url_for('index'))

@app.route('/carrito')
def carrito():
    if 'carrito' not in session or not session['carrito']:
        return render_template('carrito.html', productos=[], total=0)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM productos WHERE id IN %s;', (tuple(session['carrito']),))
    productos = cur.fetchall()
    cur.close()
    conn.close()

    # Suma los precios de los productos
    total = sum([float(p[3]) for p in productos])  # índice 3 es el campo 'precio'
    return render_template('carrito.html', productos=productos, total=total)

@app.route('/vaciar_carrito')
def vaciar_carrito():
    session['carrito'] = []
    session.modified = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)