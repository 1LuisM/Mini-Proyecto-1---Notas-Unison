from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

def init_db():
    if not os.path.exists("notas.db"):
        conn = sqlite3.connect("notas.db")
        conn.execute("""
            CREATE TABLE notas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                contenido TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

init_db()


@app.route('/')
@app.route('/index')
def index():
    integrantes = ["Luis Angel Muñiz Apodaca"]
    return render_template("index.html", integrantes=integrantes)

@app.route('/crear_nota', methods=['GET', 'POST'])
def crear_nota():
    if request.method == 'POST':
        titulo = request.form['titulo']
        contenido = request.form['contenido']

        if titulo.strip() == "" or contenido.strip() == "":
            return render_template('crear_nota.html', error="Todos los campos son obligatorios")

        conn = sqlite3.connect("notas.db")
        conn.execute("INSERT INTO notas (titulo, contenido) VALUES (?, ?)", (titulo, contenido))
        conn.commit()
        conn.close()

        return redirect(url_for('listar_notas'))
    return render_template('crear_nota.html')

@app.route('/listar_notas')
def listar_notas():
    conn = sqlite3.connect("notas.db")
    cursor = conn.execute("SELECT id, titulo FROM notas")
    notas = cursor.fetchall()
    conn.close()
    return render_template('listar_notas.html', notas=notas)

@app.route('/modificar_nota/<int:id>', methods=['GET', 'POST'])
def modificar_nota(id):
    conn = sqlite3.connect("notas.db")
    cursor = conn.execute("SELECT id, titulo, contenido FROM notas WHERE id=?", (id,))
    nota = cursor.fetchone()
    conn.close()

    if not nota:
        return "Nota no encontrada"

    if request.method == 'POST':
        nuevo_titulo = request.form['titulo']
        nuevo_contenido = request.form['contenido']
        conn = sqlite3.connect("notas.db")
        conn.execute("UPDATE notas SET titulo=?, contenido=? WHERE id=?", (nuevo_titulo, nuevo_contenido, id))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_notas'))

    return render_template('modificar_nota.html', nota=nota)

@app.route('/eliminar_nota/<int:id>', methods=['GET', 'POST'])
def eliminar_nota(id):
    conn = sqlite3.connect("notas.db")
    cursor = conn.execute("SELECT id, titulo FROM notas WHERE id=?", (id,))
    nota = cursor.fetchone()
    conn.close()

    if not nota:
        return "Nota no encontrada"

    if request.method == 'POST':
        conn = sqlite3.connect("notas.db")
        conn.execute("DELETE FROM notas WHERE id=?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_notas'))

    return render_template('eliminar_nota.html', nota=nota)

if __name__ == '__main__':
    app.run(debug=True)
