import sqlite3
from settings import DATABASE_PATH

def get_connection():
    """Maakt verbinding met de SQLite database."""
    return sqlite3.connect(DATABASE_PATH)

def create_tables():
    """Maakt de tabellen aan als ze nog niet bestaan."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titel TEXT NOT NULL,
            platform TEXT NOT NULL,
            status TEXT NOT NULL,
            datum_aangemaakt TEXT NOT NULL,
            datum_gepost TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prestaties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id INTEGER NOT NULL,
            datum_gemeten TEXT NOT NULL,
            views INTEGER NOT NULL,
            likes INTEGER NOT NULL,
            comments INTEGER NOT NULL,
            shares INTEGER NOT NULL,
            FOREIGN KEY (video_id) REFERENCES videos(id)
        )
    """)

    conn.commit()
    conn.close()
