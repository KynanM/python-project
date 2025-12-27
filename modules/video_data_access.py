# modules/video_DataAccess.py
"""
Data Access Object voor Video entiteiten.
Beheer CREATE, READ, UPDATE, DELETE operaties.
"""

from modules.database import get_connection
from modules.models import Video


def video_toevoegen(titel, platform, status, datum_aangemaakt):
    """Voegt een nieuwe video toe aan de database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO videos (titel, platform, status, datum_aangemaakt) VALUES (?, ?, ?, ?)",
        (titel, platform, status, datum_aangemaakt)
    )
    conn.commit()
    conn.close()


def videos_ophalen():
    """
    Haalt alle videos op.
    
    Returns:
        list: List van Video objecten.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, titel, platform, status, datum_aangemaakt, datum_gepost FROM videos")
    rows = cursor.fetchall()
    conn.close()
    
    # Maak Video objecten aan (instantiatie)
    return [Video(*row) for row in rows]


def video_ophalen_op_id(video_id):
    """
    Haalt een specifieke video op aan de hand van ID.
    
    Args:
        video_id (int): De ID van de video.
    
    Returns:
        Video: Video object of None als niet gevonden.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, titel, platform, status, datum_aangemaakt, datum_gepost FROM videos WHERE id = ?",
        (video_id,)
    )
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return Video(*row)
    return None


def video_updaten(video_id, titel, platform, status, datum_aangemaakt, datum_gepost):
    """Update gegevens van een bestaande video."""
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
    """Verwijdert een video uit de database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM videos WHERE id = ?", (video_id,))
    conn.commit()
    conn.close()
