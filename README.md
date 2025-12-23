# AI Video Tracker 📹📊

De **AI Video Tracker** is een Python Command Line Interface (CLI) applicatie ontworpen voor content creators om hun video-productieproces en de bijbehorende prestaties (views, likes, etc.) centraal te beheren. De applicatie maakt gebruik van een SQLite database en biedt de mogelijkheid om gegevens te exporteren naar gestylede Excel-rapporten.

## 🚀 Functionaliteiten

- **Video Management (CRUD)**: Volledige controle over je video-database (Aanmaken, Lezen, Updaten, Verwijderen).
- **Performance Tracking**: Houd statistieken bij zoals views, likes, comments en shares voor elke video op specifieke tijdstippen.
- **Data Relaties**: Maakt gebruik van een relationele database-structuur waarbij prestaties gekoppeld zijn aan video's via Foreign Keys.
- **Excel Export**: Genereer professionele Excel-overzichten met automatische opmaak en kolombreedte.
- **Object-Oriented Design**: De applicatie is opgebouwd met Python classes (`Video` en `Prestatie`) voor een schone en herbruikbare code-architectuur.

## 🛠️ Installatie & Voorbereiding

Volg deze stappen om de applicatie lokaal op te zetten:

1. **Clone de repository**:

git clone https://github.com/KynanM/python-project.git
cd python-project


2. **Maak een virtuele omgeving aan (venv)**:

python -m venv venv


3. **Activeer de virtuele omgeving**:
- **Windows**: `.\venv\Scripts\activate`
- **macOS/Linux**: `source venv/bin/activate`

4. **Installeer de benodigde packages**:

pip install -r requirements.txt


## ⚙️ Configuratie (Settings)

Om de veiligheid en flexibiliteit te waarborgen, maakt de applicatie gebruik van een extern instellingenbestand dat niet in de Git-repository wordt opgeslagen.

1. Zoek het bestand `settings_example.py` in de hoofdmap.
2. Kopieer dit bestand en hernoem het naar `settings.py`.
3. In `settings.py` kun je het pad naar de database aanpassen (standaard in de map `data/`).

**Let op:** Het bestand `settings.py` wordt genegeerd door Git via het `.gitignore` bestand om te voorkomen dat lokale paden of gevoelige data online komen te staan.

## 💻 Gebruik

Start de applicatie door het hoofdbestand uit te voeren:

python main.py


Bij de eerste start zal de applicatie automatisch de database (`video_tracker.db`) en de benodigde tabellen aanmaken in de geconfigureerde map. Navigeer door het programma met de cijfers in het menu.

## 📁 Projectstructuur

python-project/
├── data/ # Locatie van de SQLite database
├── modules/ # Python packages en modules
│ ├── database.py # Database connectie en init
│ ├── models.py # Class definities (Video, Prestatie)
│ ├── video_DA.py # Data Access voor Video's
│ ├── prestatie_DA.py # Data Access voor Prestaties
│ └── excel_export.py # Excel export functionaliteit
├── main.py # Startpunt van de applicatie
├── settings.py # Lokale configuratie (niet in git)
├── settings_example.py # Voorbeeld voor configuratie
├── requirements.txt # Externe dependencies (openpyxl)
└── .gitignore # Bestanden uitgesloten van versiebeheer


## 📝 Licentie & Auteur

Ontwikkeld als onderdeel van de Python Project opdracht. 
- **Auteur**: KynanM
- **Expertise**: Python 3.x, SQLite, Git workflow.
