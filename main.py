from modules.database import create_tables
from modules.video_DataAccess import video_toevoegen, videos_ophalen

def toon_menu():
    print("\n--- AI Video Tracker ---")
    print("1. Video toevoegen")
    print("2. Videos tonen")
    print("0. Stoppen")

def vraag_video_gegevens():
    titel = input("Titel: ").strip()
    platform = input("Platform (TikTok/Instagram/YouTube): ").strip()
    status = input("Status (concept/in_productie/klaar/gepost): ").strip()
    datum_aangemaakt = input("Datum aangemaakt (YYYY-MM-DD): ").strip()
    return titel, platform, status, datum_aangemaakt

def toon_videos():
    rows = videos_ophalen()
    if len(rows) == 0:
        print("Geen videos gevonden.")
    else:
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}")

def main():
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
        elif keuze == "0":
            print("Programma stopt.")
        else:
            print("Ongeldige keuze.")

if __name__ == "__main__":
    main()
