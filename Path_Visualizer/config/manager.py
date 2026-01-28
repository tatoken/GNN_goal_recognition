from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

from .defaults import *

class SettingsManager:
    """
    Gestore centralizzato delle configurazioni e delle risorse grafiche.

    Questa classe (Singleton) espone:
    1. Parametri di configurazione (Dimensioni, Scale, Directory).
    2. Palette colori in formato QColor (per QPainter/Scene grafiche).

    Attributes:
        WINDOW_TITLE (str): Titolo della finestra.
        WINDOW_SIZE (Tuple[int, int]): Dimensioni finestra.
        EXPORT_SCALE (float): Scala esportazione immagini.
        OUTPUT_DIR (str): Cartella output.
        CELL_SIZE (int): Dimensione celle griglia.
        PALETTE (Dict[str, str]): Dizionario colori Hex/Stringa.
        qcolors (Dict[str, QColor]): Dizionario colori convertiti in oggetti QColor.
    """

    def __init__(self):
        """
        Inizializza il manager caricando i valori di default e convertendo i colori.
        """
        # Caricamento configurazioni generali
        self.WINDOW_TITLE = DEFAULTS_MAIN_VALUE["WINDOW_TITLE"]
        self.WINDOW_SIZE = DEFAULTS_MAIN_VALUE["WINDOW_SIZE"]
        self.EXPORT_SCALE = DEFAULTS_MAIN_VALUE["EXPORT_SCALE"]
        self.OUTPUT_DIR = DEFAULTS_MAIN_VALUE["OUTPUT_DIR"]
        self.CELL_SIZE = DEFAULTS_MAIN_VALUE["CELL_SIZE"]
        self.BG_COLOR_UI = DEFAULTS_MAIN_VALUE["BG_COLOR_UI"]

        # Caricamento Palette
        self.PALETTE = COLOR_PALETTE

        # Generazione QColors
        self.qcolors = {}
        for key, val in self.PALETTE.items():
            if val == "transparent":
                self.qcolors[key] = Qt.GlobalColor.transparent
            else:
                self.qcolors[key] = QColor(val)
