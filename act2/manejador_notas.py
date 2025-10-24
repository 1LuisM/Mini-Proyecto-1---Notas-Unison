import sqlite3

class Nota:
    def __init__(self, titulo, contenido, id=None):
        self.id = id
        self.titulo = titulo
        self.contenido = contenido

class ManejadorDeNotas:
    def __init__(self, db_name='notasBD.db'):
        self.db_name = db_name
        self._crear_tabla()

    def _crear_tabla(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    contenido TEXT NOT NULL
                )
            ''')
            conn.commit()

    def crear_nota(self, nota):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO notas (titulo, contenido) VALUES (?, ?)',
                           (nota.titulo, nota.contenido))
            conn.commit()
            nota.id = cursor.lastrowid
            return nota

    def leer_nota(self, nota_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, titulo, contenido FROM notas WHERE id = ?', (nota_id,))
            fila = cursor.fetchone()
            if fila:
                return Nota(fila[1], fila[2], fila[0])
            return None

    def actualizar_nota(self, nota):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE notas SET titulo = ?, contenido = ? WHERE id = ?
            ''', (nota.titulo, nota.contenido, nota.id))
            conn.commit()

    def eliminar_nota(self, nota_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM notas WHERE id = ?', (nota_id,))
            conn.commit()