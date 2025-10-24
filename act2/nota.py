import os
import sqlite3
import pytest
from manejador_notas import Nota, ManejadorDeNotas

DB_TEST = 'notasTestBD.db'

@pytest.fixture(autouse=True)
def limpiar_db():
    # Asegura que la tabla esté limpia antes de cada prueba
    manejador = ManejadorDeNotas(DB_TEST)
    with sqlite3.connect(DB_TEST) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM notas')
        conn.commit()

def test_crear_nota():
    manejador = ManejadorDeNotas(DB_TEST)
    nota = Nota("Título de prueba", "Contenido de prueba")
    nota_creada = manejador.crear_nota(nota)
    assert nota_creada.id is not None

def test_leer_nota():
    manejador = ManejadorDeNotas(DB_TEST)
    nota = Nota("Leer Nota", "Contenido")
    nota_creada = manejador.crear_nota(nota)
    nota_leida = manejador.leer_nota(nota_creada.id)
    assert nota_leida is not None
    assert nota_leida.titulo == "Leer Nota"
    assert nota_leida.contenido == "Contenido"

def test_actualizar_nota():
    manejador = ManejadorDeNotas(DB_TEST)
    nota = Nota("Original", "Contenido original")
    nota = manejador.crear_nota(nota)
    nota.titulo = "Actualizado"
    nota.contenido = "Contenido actualizado"
    manejador.actualizar_nota(nota)
    nota_actualizada = manejador.leer_nota(nota.id)
    assert nota_actualizada.titulo == "Actualizado"
    assert nota_actualizada.contenido == "Contenido actualizado"

def test_eliminar_nota():
    manejador = ManejadorDeNotas(DB_TEST)
    nota = Nota("Eliminar", "Eliminar esta nota")
    nota = manejador.crear_nota(nota)
    manejador.eliminar_nota(nota.id)
    nota_eliminada = manejador.leer_nota(nota.id)
    assert nota_eliminada is None