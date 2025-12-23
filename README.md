# AI Video Tracker 📹📊

De **AI Video Tracker** is een Python Command Line Interface (CLI) applicatie waarmee content creators hun video-productie en prestaties (views, likes, etc.) centraal beheren. De app gebruikt een SQLite database en kan gestylede rapporten exporteren naar Excel.

## 🚀 Functionaliteiten

- **Video & Performance Management**: Volledige CRUD-ondersteuning voor video's en hun statistieken [file:1].
- **Data Relaties**: Gekoppelde tabellen via Foreign Keys (één video kan meerdere metingen hebben) [web:7].
- **Excel Export**: Genereer rapporten met automatische opmaak in een aparte `exports/` map [web:140].
- **Object-Oriented**: Gebruik van `Video` en `Prestatie` classes voor gestructureerde dataverwerking [file:1].

## 🛠️ Snelle Start (Voor de Docent)

Volg deze stappen om de applicatie met de **voorbeeldgegevens** direct te testen:

1. **Clone & Navigeer**:

git clone https://github.com/KynanM/python-project.git
cd python-project


2. **Setup Omgeving**:

python -m venv venv

Activeer (Windows): .\venv\Scripts\activate
Activeer (Mac/Linux): source venv/bin/activate
pip install -r requirements.txt


3. **Configuratie**:
- Maak een bestand `settings.py` aan in de hoofdmap.
- Kopieer de volgende regel erin om de voorbeelddata te gebruiken:
  ```
  DATABASE_PATH = "data/sample_data.db"
  ```

4. **Starten**:

python main.py


## ⚙️ Instellingen (settings.py)
De applicatie kijkt naar `settings.py` voor het databasepad. 
- Gebruik `data/sample_data.db` voor de evaluatie (bevat reeds data) [file:1].

*Let op: `settings.py` staat in de `.gitignore` en wordt niet geüpload naar GitHub.* [file:1]

## 📁 Projectstructuur

```text
python-project/
├── data/                    # Map voor databases (bevat sample_data.db)
├── exports/                 # Map voor Excel-exports (automatisch aangemaakt)
├── modules/                 # Python package met alle logica
│   ├── __init__.py          # Maakt van deze map een package
│   ├── database.py          # Database connectie & tabel creatie
│   ├── models.py            # Classes (Video en Prestatie)
│   ├── video_DataAccess.py     # Database functies voor video's
│   ├── prestatie_DataAccess.py # Database functies voor prestaties
│   └── excel_export.py         # Logica voor Excel rapportages
├── main.py                  # Hoofdmenu van de applicatie (CLI)
├── settings_example.py      # Voorbeeldinstellingen voor de docent
├── requirements.txt         # Lijst met externe bibliotheken (openpyxl)
└── .gitignore               # Vertelt git welke bestanden te negeren


## 📝 Auteur
Ontwikkeld door **KynanM** als eindopdracht voor de cursus Python [file:1].
