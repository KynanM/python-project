import sqlite3

from modules.database import create_tables
from modules.video_DataAccess import (
    video_toevoegen,
    videos_ophalen,
    video_ophalen_op_id,
    video_updaten,
    video_verwijderen
)

from modules.prestatie_DataAccess import (
    prestatie_toevoegen,
    prestaties_ophalen,
    prestatie_ophalen_op_id,
    prestatie_updaten,
    prestatie_verwijderen
)


def toon_menu():
    """Toont het hoofdmenu in de terminal."""
    print("\n--- AI Video Tracker ---")
    print("1. Video toevoegen")
    print("2. Videos tonen")
    print("3. Video updaten")
    print("4. Video verwijderen")
    print("5. Prestatie toevoegen")
    print("6. Prestaties tonen")
    print("7. Prestatie updaten")
    print("8. Prestatie verwijderen")
    print("0. Stoppen")


def vraag_video_id():
    """Vraagt een video id en zet het om naar int als het geldig is."""
    tekst = input("Geef video id: ").strip()
    if tekst.isdigit():
        return int(tekst)
    return None


def vraag_video_gegevens():
    """Vraagt de gegevens voor een nieuwe video."""
    titel = input("Titel: ").strip()
    platform = input("Platform (TikTok/Instagram/YouTube): ").strip()
    status = input("Status (concept/in_productie/klaar/gepost): ").strip()
    datum_aangemaakt = input("Datum aangemaakt (YYYY-MM-DD): ").strip()

    # Minimale validatie (leeg = ongeldig)
    if titel == "" or platform == "" or status == "" or datum_aangemaakt == "":
        return None

    return titel, platform, status, datum_aangemaakt


def toon_videos():
    """Toont alle videos."""
    rows = videos_ophalen()
    if len(rows) == 0:
        print("Geen videos gevonden.")
        return

    print("\nID | Titel | Platform | Status | Aangemaakt | Gepost")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}")


def update_video_flow():
    """Afhandeling voor optie 'video updaten'."""
    video_id = vraag_video_id()
    if video_id is None:
        print("Ongeldig id.")
        return

    huidige = video_ophalen_op_id(video_id)
    if huidige is None:
        print("Geen video gevonden met dit id.")
        return

    print("\nHuidige waarden:")
    print(f"{huidige[0]} | {huidige[1]} | {huidige[2]} | {huidige[3]} | {huidige[4]} | {huidige[5]}")

    print("\nNieuwe waarden invullen (druk Enter om te behouden).")
    titel = input(f"Titel [{huidige[1]}]: ").strip()
    platform = input(f"Platform [{huidige[2]}]: ").strip()
    status = input(f"Status [{huidige[3]}]: ").strip()
    datum_aangemaakt = input(f"Datum aangemaakt [{huidige[4]}]: ").strip()
    datum_gepost = input(f"Datum gepost [{huidige[5]}]: ").strip()

    if titel == "":
        titel = huidige[1]
    if platform == "":
        platform = huidige[2]
    if status == "":
        status = huidige[3]
    if datum_aangemaakt == "":
        datum_aangemaakt = huidige[4]
    if datum_gepost == "":
        datum_gepost = huidige[5]

    video_updaten(video_id, titel, platform, status, datum_aangemaakt, datum_gepost)
    print("Video bijgewerkt.")


def delete_video_flow():
    """Afhandeling voor optie 'video verwijderen'."""
    video_id = vraag_video_id()
    if video_id is None:
        print("Ongeldig id.")
        return

    huidige = video_ophalen_op_id(video_id)
    if huidige is None:
        print("Geen video gevonden met dit id.")
        return

    bevestig = input(f"Ben je zeker dat je '{huidige[1]}' wil verwijderen? (j/n): ").strip().lower()
    if bevestig == "j":
        video_verwijderen(video_id)
        print("Video verwijderd.")
    else:
        print("Verwijderen geannuleerd.")


def vraag_prestatie_id():
    tekst = input("Geef prestatie id: ").strip()
    if tekst.isdigit():
        return int(tekst)
    return None


def vraag_prestatie_gegevens():
    video_id_txt = input("Video id: ").strip()
    if not video_id_txt.isdigit():
        return None

    video_id = int(video_id_txt)
    if video_ophalen_op_id(video_id) is None:
        print("Deze video bestaat niet. Kies een bestaand video id via 'Videos tonen'.")
        return None

    datum_gemeten = input("Datum gemeten (YYYY-MM-DD): ").strip()

    views_txt = input("Views: ").strip()
    likes_txt = input("Likes: ").strip()
    comments_txt = input("Comments: ").strip()
    shares_txt = input("Shares: ").strip()

    if datum_gemeten == "":
        return None
    if not (views_txt.isdigit() and likes_txt.isdigit() and comments_txt.isdigit() and shares_txt.isdigit()):
        return None

    views = int(views_txt)
    likes = int(likes_txt)
    comments = int(comments_txt)
    shares = int(shares_txt)

    return video_id, datum_gemeten, views, likes, comments, shares


def toon_prestaties():
    rows = prestaties_ophalen()
    if len(rows) == 0:
        print("Geen prestaties gevonden.")
        return

    print("\nID | Video titel | Datum | Views | Likes | Comments | Shares")
    print("-" * 70)
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]}")


def update_prestatie_flow():
    prestatie_id = vraag_prestatie_id()
    if prestatie_id is None:
        print("Ongeldig id.")
        return

    huidige = prestatie_ophalen_op_id(prestatie_id)
    if huidige is None:
        print("Geen prestatie gevonden met dit id.")
        return

    print("\nNieuwe waarden invullen (druk Enter om te behouden).")
    video_id = input(f"Video id [{huidige[1]}]: ").strip()
    datum = input(f"Datum gemeten [{huidige[2]}]: ").strip()
    views = input(f"Views [{huidige[3]}]: ").strip()
    likes = input(f"Likes [{huidige[4]}]: ").strip()
    comments = input(f"Comments [{huidige[5]}]: ").strip()
    shares = input(f"Shares [{huidige[6]}]: ").strip()

    if video_id == "":
        video_id = huidige[1]
    elif video_id.isdigit():
        video_id = int(video_id)
        if video_ophalen_op_id(video_id) is None:
            print("Deze video bestaat niet.")
            return
    else:
        print("Ongeldige video id.")
        return

    if datum == "":
        datum = huidige[2]

    if views == "":
        views = huidige[3]
    elif views.isdigit():
        views = int(views)
    else:
        print("Ongeldige views.")
        return

    if likes == "":
        likes = huidige[4]
    elif likes.isdigit():
        likes = int(likes)
    else:
        print("Ongeldige likes.")
        return

    if comments == "":
        comments = huidige[5]
    elif comments.isdigit():
        comments = int(comments)
    else:
        print("Ongeldige comments.")
        return

    if shares == "":
        shares = huidige[6]
    elif shares.isdigit():
        shares = int(shares)
    else:
        print("Ongeldige shares.")
        return

    prestatie_updaten(prestatie_id, video_id, datum, views, likes, comments, shares)
    print("Prestatie bijgewerkt.")


def delete_prestatie_flow():
    prestatie_id = vraag_prestatie_id()
    if prestatie_id is None:
        print("Ongeldig id.")
        return

    huidige = prestatie_ophalen_op_id(prestatie_id)
    if huidige is None:
        print("Geen prestatie gevonden met dit id.")
        return

    bevestig = input(f"Ben je zeker dat je prestatie {prestatie_id} wil verwijderen? (j/n): ").strip().lower()
    if bevestig == "j":
        prestatie_verwijderen(prestatie_id)
        print("Prestatie verwijderd.")
    else:
        print("Verwijderen geannuleerd.")


def main():
    """Startpunt van de applicatie."""
    create_tables()

    keuze = None
    while keuze != "0":
        toon_menu()
        keuze = input("Kies een optie: ").strip()

        if keuze == "1":
            data = vraag_video_gegevens()
            if data is None:
                print("Ongeldige invoer.")
                continue
            video_toevoegen(*data)
            print("Video toegevoegd.")

        elif keuze == "2":
            toon_videos()

        elif keuze == "3":
            update_video_flow()

        elif keuze == "4":
            delete_video_flow()

        elif keuze == "5":
            data = vraag_prestatie_gegevens()
            if data is None:
                print("Ongeldige invoer.")
                continue
            try:
                prestatie_toevoegen(*data)
                print("Prestatie toegevoegd.")
            except sqlite3.IntegrityError:
                print("Kon prestatie niet toevoegen (controleer video id en unieke datum).")
            except sqlite3.OperationalError:
                print("Database is momenteel vergrendeld. Sluit andere programma's en probeer opnieuw.")

        elif keuze == "6":
            toon_prestaties()

        elif keuze == "7":
            update_prestatie_flow()

        elif keuze == "8":
            delete_prestatie_flow()

        elif keuze == "0":
            print("Programma stopt.")
        else:
            print("Ongeldige keuze.")


if __name__ == "__main__":
    main()
