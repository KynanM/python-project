# modules/prestatie_DataAccess.py
"""
Data Access Object voor Prestatie entiteiten.
Beheer CREATE, READ, UPDATE, DELETE operaties.
"""

from modules.database import get_connection
from modules.models import Prestatie


def prestatie_toevoegen(video_id, datum_gemeten, views, likes, comments, shares):
    """Voegt een nieuwe prestatie (metric) toe."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO prestaties (video_id, datum_gemeten, views, likes, comments, shares)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (video_id, datum_gemeten, views, likes, comments, shares)
    )
    conn.commit()
    conn.close()


def prestaties_ophalen():
    """
    Haalt alle prestaties op inclusief videotitel (via JOIN).
    
    Returns:
        list: List van Prestatie objecten.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT p.id, p.video_id, p.datum_gemeten, p.views, p.likes, p.comments, p.shares, v.titel
        FROM prestaties p
        JOIN videos v ON v.id = p.video_id
        ORDER BY p.datum_gemeten DESC, p.id DESC
        """
    )
    rows = cursor.fetchall()
    conn.close()
    
    # Maak Prestatie objecten aan (instantiatie)
    # row is: (id, video_id, datum_gemeten, views, likes, comments, shares, titel)
    prestaties = []
    for row in rows:
        prestatie = Prestatie(
            id=row[0],
            video_id=row[1],
            datum_gemeten=row[2],
            views=row[3],
            likes=row[4],
            comments=row[5],
            shares=row[6],
            video_titel=row[7]
        )
        prestaties.append(prestatie)
    
    return prestaties


def prestatie_ophalen_op_id(prestatie_id):
    """
    Haalt een specifieke prestatie op.
    
    Args:
        prestatie_id (int): De ID van de prestatie.
    
    Returns:
        Prestatie: Prestatie object of None als niet gevonden.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT p.id, p.video_id, p.datum_gemeten, p.views, p.likes, p.comments, p.shares, v.titel
        FROM prestaties p
        LEFT JOIN videos v ON v.id = p.video_id
        WHERE p.id = ?
        """,
        (prestatie_id,)
    )
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return Prestatie(
            id=row[0],
            video_id=row[1],
            datum_gemeten=row[2],
            views=row[3],
            likes=row[4],
            comments=row[5],
            shares=row[6],
            video_titel=row[7]
        )
    return None


def prestatie_updaten(prestatie_id, video_id, datum_gemeten, views, likes, comments, shares):
    """Update gegevens van een bestaande prestatie."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE prestaties
        SET video_id = ?, datum_gemeten = ?, views = ?, likes = ?, comments = ?, shares = ?
        WHERE id = ?
        """,
        (video_id, datum_gemeten, views, likes, comments, shares, prestatie_id)
    )
    conn.commit()
    conn.close()


def prestatie_verwijderen(prestatie_id):
    """Verwijdert een prestatie uit de database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM prestaties WHERE id = ?", (prestatie_id,))
    conn.commit()
    conn.close()
