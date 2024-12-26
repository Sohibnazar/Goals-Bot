import sqlite3


def init_db():
    conn = sqlite3.connect("goals.db")
    cursor = conn.cursor()

    # Таблица для целей
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            deadline DATE,
            status TEXT DEFAULT 'in_progress'
        )
    """)


    conn.commit()
    conn.close()

# 1) Добавление цели
def add_goal(description, deadline):
    conn = sqlite3.connect("goals.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO goals (description, deadline) VALUES (?, ?)", (description, deadline))
    conn.commit()
    conn.close()

