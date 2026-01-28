"""
File di definizione delle costanti e dei valori predefiniti.

Questo modulo funge da 'single source of truth' per i valori statici
dell'applicazione. Contiene una singola palette colori unificata.
"""

from PyQt6.QtCore import Qt

DEFAULTS_MAIN_VALUE = {
    "WINDOW_TITLE": "Path + Heatmap Visualizer",
    "WINDOW_SIZE": (1300, 700),
    "EXPORT_SCALE": 3.0,
    "OUTPUT_DIR": "visual_result",
    "CELL_SIZE": 50,
    "BG_COLOR_UI": "#2c3e50" 
}

COLOR_PALETTE = {
    "BG_EMPTY": "#ecf0f1",     # Cella vuota
    "WALL": "#34495e",         # Muro/Ostacolo
    "START": "#2ecc71",        # Punto di partenza (Verde)
    "GOAL": "#e74c3c",         # Destinazione (Rosso)
    "PATH": "#3498db",         # Percorso calcolato (Blu)
    "TEXT": "#7f8c8d",         # Testo nelle celle
    "GRID": "#bdc3c7",         # Linee griglia
    "TEXT_HL": "#ffffff",      # Testo evidenziato (es. su path)
    "TRANSPARENT": "transparent"
}