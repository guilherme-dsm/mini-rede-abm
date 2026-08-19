import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
    return conn

def criar_tabelas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predios (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            bloco TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS moradores (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            predio_id INTEGER NOT NULL,
            apartamento TEXT NOT NULL,
            foto_perfil TEXT,
            FOREIGN KEY (predio_id) REFERENCES predios (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            autor_id INTEGER NOT NULL,
            categoria TEXT NOT NULL,
            titulo TEXT NOT NULL,
            conteudo TEXT NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (autor_id) REFERENCES moradores (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS redefinicoes_senha (
            id SERIAL PRIMARY KEY,
            morador_id INTEGER NOT NULL,
            token TEXT NOT NULL UNIQUE,
            expira_em TIMESTAMP NOT NULL,
            usado INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (morador_id) REFERENCES moradores (id)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()