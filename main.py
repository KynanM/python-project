from modules.database import create_tables
from modules.video_DataAccess import (
    video_toevoegen,
    videos_ophalen,
    video_ophalen_op_id,
    video_updaten,
    video_verwijderen
)


def toon_menu():
    """Toont het hoofdmenu in de terminal."""
    print("\n--- AI Video Tracker ---")
    print("1. Video toevoegen")
    print("2. Videos tonen")
    print("3. Video updaten")
    print("4. Video verwijderen")
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
        # row is een tuple: (id, titel, platform, status, datum_aangemaakt, datum_gepost)
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

    # Als gebruiker niets ingeeft: behoud de huidige waarde
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


def main():
    """Startpunt van de applicatie."""
    create_tables()

    keuze = None
    while keuze != "0":
        toon_menu()
        keuze = input("Kies een optie: ").strip()

        if keuze == "1":
            titel, platform, status, datum_aangemaakt = vraag_video_gegevens()
            video_toevoegen(titel, platform, status, datum_aangemaakt)
            print("Video toegevoegd.")
        elif keuze == "2":
            toon_videos()
        elif keuze == "3":
            update_video_flow()
        elif keuze == "4":
            delete_video_flow()
        elif keuze == "0":
            print("Programma stopt.")
        else:
            print("Ongeldige keuze.")


if __name__ == "__main__":
    main()