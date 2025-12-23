# modules/models.py
"""
Data model classes voor Video's en Prestaties.
Deze classes representeren de entiteiten uit de database.
"""

class Video:
    """Representeert een video uit de database."""
    
    def __init__(self, id, titel, platform, status, datum_aangemaakt, datum_gepost=None):
        self.id = id
        self.titel = titel
        self.platform = platform
        self.status = status
        self.datum_aangemaakt = datum_aangemaakt
        self.datum_gepost = datum_gepost
    
    def __repr__(self):
        """Voor debugging: toont een overzicht van het Video-object."""
        return (f"Video(id={self.id}, titel='{self.titel}', "
                f"platform='{self.platform}', status='{self.status}')")


class Prestatie:
    """Representeert de statistieken (metrics) van een video op een bepaald moment."""
    
    def __init__(self, id, video_id, datum_gemeten, views, likes, comments, shares, video_titel=None):
        self.id = id
        self.video_id = video_id
        self.datum_gemeten = datum_gemeten
        self.views = views
        self.likes = likes
        self.comments = comments
        self.shares = shares
        self.video_titel = video_titel  # Wordt ingevuld via JOIN in DataAccess
    
    def __repr__(self):
        """Voor debugging: toont een overzicht van het Prestatie-object."""
        return (f"Prestatie(id={self.id}, video_titel='{self.video_titel}', "
                f"datum='{self.datum_gemeten}', views={self.views})")
