from models.db import get_connection, criar_tabelas

PREDIOS = [
    ("Estela do Mar", "bloco 1"),
    ("Estela do Mar", "bloco 2"),
    ("Barra D'Oro", "bloco 1"),
    ("Mar de Prata", None),
    ("Barra One", "bloco 1"),
]

def seed():
    criar_tabelas()
    conn = get_connection()
    cursor = conn.cursor()

    for nome, bloco in PREDIOS:
        cursor.execute(
            "SELECT id FROM predios WHERE nome = ? AND bloco IS ?",
            (nome, bloco)
        )
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO predios (nome, bloco) VALUES (?, ?)",
                (nome, bloco)
            )

    conn.commit()
    conn.close()
    print("Prédios cadastrados com sucesso.")

if __name__ == "__main__":
    seed()
