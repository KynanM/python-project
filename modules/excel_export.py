# modules/excel_export.py
"""
Excel export tool voor het exporteren van video's en prestaties.
Slaat bestanden automatisch op in de map 'exports/'.
"""
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import datetime
from modules.video_DataAccess import videos_ophalen
from modules.prestatie_DataAccess import prestaties_ophalen

# De map waarin alle excels worden opgeslagen
EXPORT_DIR = "exports"

def _format_header(ws, row_num):
    """Formatteer de header-rij met vet lettertype en achtergrondkleur."""
    fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    font = Font(bold=True, color="FFFFFF")
    alignment = Alignment(horizontal="center", vertical="center")
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    for cell in ws[row_num]:
        if cell.value:
            cell.fill = fill
            cell.font = font
            cell.alignment = alignment
            cell.border = border

def _prepare_path(bestandsnaam, standaard_prefix):
    """Zorgt dat de export-map bestaat en geeft het volledige pad terug."""
    # 1. Maak de map aan als deze nog niet bestaat
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)
    
    # 2. Bepaal standaard bestandsnaam indien nodig
    if bestandsnaam is None:
        datum = datetime.now().strftime("%Y-%m-%d")
        bestandsnaam = f"{standaard_prefix}_{datum}.xlsx"
    
    # 3. Koppel de map aan de bestandsnaam
    return os.path.join(EXPORT_DIR, bestandsnaam)

def exporteer_videos_excel(bestandsnaam=None):
    """Exporteert alle videos naar een Excel bestand in de exports map."""
    volledig_pad = _prepare_path(bestandsnaam, "export_videos")
    
    videos = videos_ophalen()
    wb = Workbook()
    ws = wb.active
    ws.title = "Videos"
    
    headers = ["ID", "Titel", "Platform", "Status", "Datum Aangemaakt", "Datum Gepost"]
    ws.append(headers)
    _format_header(ws, 1)
    
    for video in videos:
        ws.append([
            video.id, video.titel, video.platform, video.status,
            video.datum_aangemaakt, video.datum_gepost if video.datum_gepost else "-"
        ])
    
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except: pass
        ws.column_dimensions[column_letter].width = max_length + 2
    
    wb.save(volledig_pad)
    return volledig_pad

def exporteer_prestaties_excel(bestandsnaam=None):
    """Exporteert alle prestaties naar een Excel bestand in de exports map."""
    volledig_pad = _prepare_path(bestandsnaam, "export_prestaties")
    
    prestaties = prestaties_ophalen()
    wb = Workbook()
    ws = wb.active
    ws.title = "Prestaties"
    
    headers = ["ID", "Video Titel", "Datum Gemeten", "Views", "Likes", "Comments", "Shares"]
    ws.append(headers)
    _format_header(ws, 1)
    
    for prestatie in prestaties:
        ws.append([
            prestatie.id, prestatie.video_titel, prestatie.datum_gemeten,
            prestatie.views, prestatie.likes, prestatie.comments, prestatie.shares
        ])
    
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except: pass
        ws.column_dimensions[column_letter].width = max_length + 2
    
    wb.save(volledig_pad)
    return volledig_pad

def exporteer_alles_excel(bestandsnaam=None):
    """Exporteert ALLES naar één Excel bestand in de exports map."""
    volledig_pad = _prepare_path(bestandsnaam, "export_compleet")
    
    videos = videos_ophalen()
    prestaties = prestaties_ophalen()
    
    wb = Workbook()
    wb.remove(wb.active)
    
    # SHEET 1: Videos
    ws_v = wb.create_sheet("Videos")
    ws_v.append(["ID", "Titel", "Platform", "Status", "Datum Aangemaakt", "Datum Gepost"])
    _format_header(ws_v, 1)
    for v in videos:
        ws_v.append([v.id, v.titel, v.platform, v.status, v.datum_aangemaakt, v.datum_gepost or "-"])
    
    # SHEET 2: Prestaties
    ws_p = wb.create_sheet("Prestaties")
    ws_p.append(["ID", "Video Titel", "Datum Gemeten", "Views", "Likes", "Comments", "Shares"])
    _format_header(ws_p, 1)
    for p in prestaties:
        ws_p.append([p.id, p.video_titel, p.datum_gemeten, p.views, p.likes, p.comments, p.shares])
    
    # Automatische kolombreedte voor beide sheets
    for ws in wb.worksheets:
        for column in ws.columns:
            max_len = max((len(str(cell.value)) for cell in column if cell.value), default=0)
            ws.column_dimensions[column[0].column_letter].width = max_len + 2
            
    wb.save(volledig_pad)
    return volledig_pad
