import unittest
import os
import sqlite3
import modules.database as db
import modules.video_data_access as vda
import modules.prestatie_data_access as pda
from modules.excel_export import exporteer_alles_excel

class TestTrackerVolledig(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Maak een specifiek test-database pad aan."""
        cls.test_db = "test_database_temp.db"
        # Forceer het pad in de database module DIRECT
        import modules.database
        modules.database.DATABASE_PATH = cls.test_db

    def setUp(self):
        """Maak de tabellen leeg voor elke test zonder het bestand te verwijderen."""
        db.create_tables() # Zorg dat ze bestaan
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        # Zet foreign keys uit om alles zonder volgorde-fouten te kunnen wissen
        cursor.execute("PRAGMA foreign_keys = OFF")
        cursor.execute("DELETE FROM prestaties")
        cursor.execute("DELETE FROM videos")
        cursor.execute("PRAGMA foreign_keys = ON")
        conn.commit()
        conn.close()

    def tearDown(self):
        """Verwijder tijdelijke Excel bestanden."""
        # Check beide locaties voor de zekerheid
        for pad in ["test_export.xlsx", os.path.join("exports", "test_export.xlsx")]:
            if os.path.exists(pad):
                try:
                    os.remove(pad)
                except PermissionError:
                    pass


    @classmethod
    def tearDownClass(cls):
        """Verwijder de test-db na afloop van alle tests."""
        # Probeer te verwijderen, maar negeer fouten als Windows het bestand lockt
        try:
            if os.path.exists(cls.test_db):
                os.remove(cls.test_db)
        except PermissionError:
            print(f"\nInfo: Kon {cls.test_db} niet direct verwijderen (bestand gelockt door Windows).")

    def test_performance_crud_volledig(self):
        """Test of prestaties correct worden opgeslagen en getoond met videotitel."""
        vda.video_toevoegen("Test Video", "TikTok", "gepost", "2025-01-01")
        vid = vda.videos_ophalen()[0].id
        
        pda.prestatie_toevoegen(vid, "2025-12-23", 500, 50, 5, 2)
        
        prestaties = pda.prestaties_ophalen()
        self.assertEqual(len(prestaties), 1)
        self.assertEqual(prestaties[0].video_titel, "Test Video")

    def test_excel_export_file_creation(self):
        """Test of de Excel export daadwerkelijk een bestand aanmaakt."""
        vda.video_toevoegen("Export Video", "YouTube", "klaar", "2025-01-01")
        
        bestandsnaam = "test_export.xlsx"
        
        resultaat_pad = exporteer_alles_excel(bestandsnaam)
        
        self.assertTrue(os.path.exists(resultaat_pad))
        
        self.assertTrue(resultaat_pad.endswith(bestandsnaam))


    def test_cascade_delete(self):
        """Test of prestaties verdwijnen als de video wordt verwijderd (CASCADE)."""
        vda.video_toevoegen("Delete Me", "Instagram", "klaar", "2025-01-01")
        vid = vda.videos_ophalen()[0].id
        pda.prestatie_toevoegen(vid, "2025-12-23", 10, 1, 0, 0)
        
        self.assertEqual(len(pda.prestaties_ophalen()), 1)
        vda.video_verwijderen(vid)
        
        # Bij een correcte ON DELETE CASCADE is dit nu 0
        self.assertEqual(len(pda.prestaties_ophalen()), 0)

if __name__ == '__main__':
    unittest.main()
