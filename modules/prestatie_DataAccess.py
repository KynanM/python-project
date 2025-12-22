from modules.database import get_connection


def prestatie_toevoegen(video_id, datum_gemeten, views, likes, comments, shares):
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
    """Haalt alle prestaties op, inclusief videotitel (JOIN)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT p.id, v.titel, p.datum_gemeten, p.views, p.likes, p.comments, p.shares
        FROM prestaties p
        JOIN videos v ON v.id = p.video_id
        ORDER BY p.datum_gemeten DESC, p.id DESC
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def prestatie_ophalen_op_id(prestatie_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, video_id, datum_gemeten, views, likes, comments, shares
        FROM prestaties
        WHERE id = ?
        """,
        (prestatie_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row


def prestatie_updaten(prestatie_id, video_id, datum_gemeten, views, likes, comments, shares):
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
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM prestaties WHERE id = ?", (prestatie_id,))
    conn.commit()
    conn.close()
