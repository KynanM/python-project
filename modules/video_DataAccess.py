from modules.database import get_connection

def video_toevoegen(titel, platform, status, datum_aangemaakt):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO videos (titel, platform, status, datum_aangemaakt) VALUES (?, ?, ?, ?)",
        (titel, platform, status, datum_aangemaakt)
    )
    conn.commit()
    conn.close()

def videos_ophalen():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, titel, platform, status, datum_aangemaakt, datum_gepost FROM videos")
    rows = cursor.fetchall()
    conn.close()
    return rows
