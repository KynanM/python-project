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

def video_updaten(video_id, titel, platform, status, datum_aangemaakt, datum_gepost):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE videos
        SET titel = ?, platform = ?, status = ?, datum_aangemaakt = ?, datum_gepost = ?
        WHERE id = ?
        """,
        (titel, platform, status, datum_aangemaakt, datum_gepost, video_id)
    )
    conn.commit()
    conn.close()

def video_verwijderen(video_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM videos WHERE id = ?", (video_id,))
    conn.commit()
    conn.close()

def video_ophalen_op_id(video_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, titel, platform, status, datum_aangemaakt, datum_gepost FROM videos WHERE id = ?",
        (video_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row