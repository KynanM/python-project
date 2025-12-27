# main.py
"""
AI Video Tracker - Main applicatie
Command-line interface voor video- en prestatie management.
"""

import sqlite3
from modules.database import create_tables
from modules.video_data_access import (
    video_toevoegen,
    videos_ophalen,
    video_ophalen_op_id,
    video_updaten,
    video_verwijderen
)
from modules.prestatie_data_access import (
    prestatie_toevoegen,
    prestaties_ophalen,
    prestatie_ophalen_op_id,
    prestatie_updaten,
    prestatie_verwijderen
)
from modules.excel_export import (
    exporteer_videos_excel,
    exporteer_prestaties_excel,
    exporteer_alles_excel
)


def toon_menu():
    """Toont het hoofdmenu in de terminal."""
    print("\n" + "=" * 50)
    print("--- AI VIDEO TRACKER ---".center(50))
    print("=" * 50)
    print("\n📹 VIDEO BEHEER")
    print("1. Video toevoegen")
    print("2. Videos tonen")
    print("3. Video updaten")
    print("4. Video verwijderen")
    print("\n📊 PRESTATIE BEHEER")
    print("5. Prestatie toevoegen")
    print("6. Prestaties tonen")
    print("7. Prestatie updaten")
    print("8. Prestatie verwijderen")
    print("\n💾 EXPORTEREN")
    print("9. Exporteer videos naar Excel")
    print("10. Exporteer prestaties naar Excel")
    print("11. Exporteer ALLES naar Excel")
    print("\n0. Stoppen")
    print("=" * 50)


def vraag_video_id():
    """Vraagt een video id en zet het om naar int als het geldig is."""
    tekst = input("Geef video id: ").strip()
    if tekst.isdigit():
        return int(tekst)
    print("❌ Ongeldig ID. Moet een getal zijn.")
    return None


def vraag_video_gegevens():
    """Vraagt de gegevens voor een nieuwe video."""
    print("\n--- Nieuwe video toevoegen ---")
    titel = input("Titel: ").strip()
    platform = input("Platform (TikTok/Instagram/YouTube): ").strip()
    status = input("Status (concept/in_productie/klaar/gepost): ").strip()
    datum_aangemaakt = input("Datum aangemaakt (YYYY-MM-DD): ").strip()

    # Minimale validatie (leeg = ongeldig)
    if not (titel and platform and status and datum_aangemaakt):
        print("❌ Alle velden zijn verplicht.")
        return None

    return titel, platform, status, datum_aangemaakt


def toon_videos():
    """Toont alle videos in een geformateerde tabel."""
    videos = videos_ophalen()  
    
    if len(videos) == 0:
        print("\n❌ Geen videos gevonden.")
        return

    print("\n" + "=" * 90)
    print(f"{'ID':<4} | {'Titel':<20} | {'Platform':<12} | {'Status':<15} | {'Aangemaakt':<12} | {'Gepost':<12}")
    print("-" * 90)
    
    for video in videos:
        gepost = video.datum_gepost if video.datum_gepost else "-"
        print(f"{video.id:<4} | {video.titel:<20} | {video.platform:<12} | {video.status:<15} | {video.datum_aangemaakt:<12} | {gepost:<12}")
    
    print("=" * 90)


def update_video_flow():
    """Afhandeling voor optie 'video updaten'."""
    video_id = vraag_video_id()
    if video_id is None:
        return

    huidige = video_ophalen_op_id(video_id)  
    if huidige is None:
        print("❌ Geen video gevonden met dit id.")
        return

    print("\n📝 Huidige waarden:")
    print(f"  Titel: {huidige.titel}")
    print(f"  Platform: {huidige.platform}")
    print(f"  Status: {huidige.status}")
    print(f"  Aangemaakt: {huidige.datum_aangemaakt}")
    print(f"  Gepost: {huidige.datum_gepost if huidige.datum_gepost else '-'}")

    print("\nNieuwe waarden invullen (druk Enter om te behouden):")
    titel = input(f"Titel [{huidige.titel}]: ").strip() or huidige.titel
    platform = input(f"Platform [{huidige.platform}]: ").strip() or huidige.platform
    status = input(f"Status [{huidige.status}]: ").strip() or huidige.status
    datum_aangemaakt = input(f"Datum aangemaakt [{huidige.datum_aangemaakt}]: ").strip() or huidige.datum_aangemaakt
    datum_gepost = input(f"Datum gepost [{huidige.datum_gepost or '-'}]: ").strip() or huidige.datum_gepost

    video_updaten(video_id, titel, platform, status, datum_aangemaakt, datum_gepost)
    print("✅ Video bijgewerkt.")


def delete_video_flow():
    """Afhandeling voor optie 'video verwijderen'."""
    video_id = vraag_video_id()
    if video_id is None:
        return

    huidige = video_ophalen_op_id(video_id) 
    if huidige is None:
        print("❌ Geen video gevonden met dit id.")
        return

    bevestig = input(f"\n⚠️  Ben je zeker dat je '{huidige.titel}' wil verwijderen? (j/n): ").strip().lower()
    if bevestig == "j":
        video_verwijderen(video_id)
        print("✅ Video verwijderd.")
    else:
        print("❌ Verwijderen geannuleerd.")


def vraag_prestatie_id():
    """Vraagt een prestatie id en zet het om naar int als het geldig is."""
    tekst = input("Geef prestatie id: ").strip()
    if tekst.isdigit():
        return int(tekst)
    print("❌ Ongeldig ID. Moet een getal zijn.")
    return None


def vraag_prestatie_gegevens():
    """Vraagt de gegevens voor een nieuwe prestatie."""
    print("\n--- Nieuwe prestatie toevoegen ---")
    video_id_txt = input("Video id: ").strip()
    if not video_id_txt.isdigit():
        print("❌ Video ID moet een getal zijn.")
        return None

    video_id = int(video_id_txt)
    if video_ophalen_op_id(video_id) is None:
        print(f"❌ Video met ID {video_id} bestaat niet. Kies een bestaand video id via 'Videos tonen'.")
        return None

    datum_gemeten = input("Datum gemeten (YYYY-MM-DD): ").strip()

    views_txt = input("Views: ").strip()
    likes_txt = input("Likes: ").strip()
    comments_txt = input("Comments: ").strip()
    shares_txt = input("Shares: ").strip()

    if not datum_gemeten:
        print("❌ Datum is verplicht.")
        return None
    
    if not (views_txt.isdigit() and likes_txt.isdigit() and comments_txt.isdigit() and shares_txt.isdigit()):
        print("❌ Views, Likes, Comments en Shares moeten getallen zijn.")
        return None

    return video_id, datum_gemeten, int(views_txt), int(likes_txt), int(comments_txt), int(shares_txt)


def toon_prestaties():
    """Toont alle prestaties in een geformateerde tabel."""
    prestaties = prestaties_ophalen()  
    
    if len(prestaties) == 0:
        print("\n❌ Geen prestaties gevonden.")
        return

    print("\n" + "=" * 100)
    print(f"{'ID':<4} | {'Video Titel':<25} | {'Datum':<12} | {'Views':<8} | {'Likes':<8} | {'Comments':<10} | {'Shares':<8}")
    print("-" * 100)
    
    for prestatie in prestaties:
        print(f"{prestatie.id:<4} | {prestatie.video_titel:<25} | {prestatie.datum_gemeten:<12} | {prestatie.views:<8} | {prestatie.likes:<8} | {prestatie.comments:<10} | {prestatie.shares:<8}")
    
    print("=" * 100)


def update_prestatie_flow():
    """Afhandeling voor optie 'prestatie updaten'."""
    prestatie_id = vraag_prestatie_id()
    if prestatie_id is None:
        return

    huidige = prestatie_ophalen_op_id(prestatie_id) 
    if huidige is None:
        print("❌ Geen prestatie gevonden met dit id.")
        return

    print("\n📝 Huidige waarden:")
    print(f"  Video: {huidige.video_titel}")
    print(f"  Datum gemeten: {huidige.datum_gemeten}")
    print(f"  Views: {huidige.views}")
    print(f"  Likes: {huidige.likes}")
    print(f"  Comments: {huidige.comments}")
    print(f"  Shares: {huidige.shares}")

    print("\nNieuwe waarden invullen (druk Enter om te behouden):")
    
    video_id = input(f"Video id [{huidige.video_id}]: ").strip()
    if video_id and video_id.isdigit():
        video_id = int(video_id)
        if video_ophalen_op_id(video_id) is None:
            print("❌ Deze video bestaat niet.")
            return
    else:
        video_id = huidige.video_id if not video_id else None
        if video_id is None:
            print("❌ Ongeldige video id.")
            return

    datum = input(f"Datum gemeten [{huidige.datum_gemeten}]: ").strip() or huidige.datum_gemeten
    views = input(f"Views [{huidige.views}]: ").strip() or huidige.views
    likes = input(f"Likes [{huidige.likes}]: ").strip() or huidige.likes
    comments = input(f"Comments [{huidige.comments}]: ").strip() or huidige.comments
    shares = input(f"Shares [{huidige.shares}]: ").strip() or huidige.shares

    # Validatie van numerieke velden
    try:
        views = int(views)
        likes = int(likes)
        comments = int(comments)
        shares = int(shares)
    except ValueError:
        print("❌ Views, Likes, Comments en Shares moeten getallen zijn.")
        return

    prestatie_updaten(prestatie_id, video_id, datum, views, likes, comments, shares)
    print("✅ Prestatie bijgewerkt.")


def delete_prestatie_flow():
    """Afhandeling voor optie 'prestatie verwijderen'."""
    prestatie_id = vraag_prestatie_id()
    if prestatie_id is None:
        return

    huidige = prestatie_ophalen_op_id(prestatie_id)  
    if huidige is None:
        print("❌ Geen prestatie gevonden met dit id.")
        return

    bevestig = input(f"\n⚠️  Ben je zeker dat je prestatie {prestatie_id} voor '{huidige.video_titel}' wil verwijderen? (j/n): ").strip().lower()
    if bevestig == "j":
        prestatie_verwijderen(prestatie_id)
        print("✅ Prestatie verwijderd.")
    else:
        print("❌ Verwijderen geannuleerd.")


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
                continue
            video_toevoegen(*data)
            print("✅ Video toegevoegd.")

        elif keuze == "2":
            toon_videos()

        elif keuze == "3":
            update_video_flow()

        elif keuze == "4":
            delete_video_flow()

        elif keuze == "5":
            data = vraag_prestatie_gegevens()
            if data is None:
                continue
            try:
                prestatie_toevoegen(*data)
                print("✅ Prestatie toegevoegd.")
            except sqlite3.IntegrityError:
                print("❌ Kon prestatie niet toevoegen (controleer video id en/of unieke datum per video).")
            except sqlite3.OperationalError:
                print("❌ Database is momenteel vergrendeld. Sluit andere programma's en probeer opnieuw.")

        elif keuze == "6":
            toon_prestaties()

        elif keuze == "7":
            update_prestatie_flow()

        elif keuze == "8":
            delete_prestatie_flow()

        elif keuze == "9":
            bestandsnaam = exporteer_videos_excel()
            print(f"✅ Videos geëxporteerd naar: {bestandsnaam}")

        elif keuze == "10":
            bestandsnaam = exporteer_prestaties_excel()
            print(f"✅ Prestaties geëxporteerd naar: {bestandsnaam}")

        elif keuze == "11":
            bestandsnaam = exporteer_alles_excel()
            print(f"✅ Alles geëxporteerd naar: {bestandsnaam}")

        elif keuze == "0":
            print("\n👋 Programma stopt. Tot ziens!")
        else:
            print("❌ Ongeldige keuze. Probeer opnieuw.")


if __name__ == "__main__":
    main()
