from PyQt6.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from ..config import settings
from PyQt6.QtGui import QPen, QBrush, QFont

class BaseGridScene(QGraphicsScene):
    """
    Classe base ottimizzata per la renderizzazione di griglie.

    Invece di distruggere e ricreare gli elementi a ogni frame (che causerebbe flickering e lentezza), 
    crea gli oggetti una volta sola e ne aggiorna solo le proprietà (colore, testo).

    Attributes:
        rects (List[List[QGraphicsRectItem]]): Matrice di riferimenti ai rettangoli grafici.
        texts (List[List[QGraphicsTextItem]]): Matrice di riferimenti alle etichette di testo.
        is_initialized (bool): Flag per tracciare se la griglia fisica è stata istanziata.
    """
    def __init__(self, map_data, cell_size=settings.CELL_SIZE):
        """
        Inizializza la scena base con i dati della mappa.

        Args:
            map_data (List[List[int]]): La matrice strutturale della mappa (es. 0/1).
            cell_size (int, optional): La dimensione in pixel per lato di ogni cella.
        """
        super().__init__()
        self.map_data = map_data
        self.map_size = len(map_data)
        self.cell_size = cell_size
        
        # Matrici per memorizzare i riferimenti agli oggetti grafici
        # Questo permette accesso O(1) nell'aggiornamento 
        self.rects = [[None for _ in range(self.map_size)] for _ in range(self.map_size)]
        self.texts = [[None for _ in range(self.map_size)] for _ in range(self.map_size)]
        
        # Flag per sapere se la griglia è già stata disegnata
        self.is_initialized = False

    def _init_grid_items(self):
        """
        Istanzia TUTTI i rettangoli e i testi una volta sola (Lazy Initialization).
        
        Questa funzione è computazionalmente pesante ma viene chiamata una sola volta.
        Popola la scena e riempie le matrici `self.rects` e `self.texts`.
        """
        self.clear()
        
        for r in range(self.map_size):
            for c in range(self.map_size):
                x, y = c * self.cell_size, r * self.cell_size
                
                # Crea la cella
                rect = QGraphicsRectItem(x, y, self.cell_size, self.cell_size)
                rect.setPen(QPen(settings.qcolors["GRID"], 1))
                rect.setBrush(QBrush(settings.qcolors["BG_EMPTY"])) 
                self.addItem(rect)
                self.rects[r][c] = rect

                # Crea l'etichetta che ospiterà il nome della cella
                t = QGraphicsTextItem("")
                font = QFont("Arial", 8)
                t.setFont(font)
                t.setDefaultTextColor(settings.qcolors["TEXT"])
                dx = (self.cell_size - 10) / 2
                dy = (self.cell_size - 20) / 2
                t.setPos(x + dx, y + dy)
                self.addItem(t)
                self.texts[r][c] = t
                
        self.is_initialized = True

    def _update_cell(self, r, c, color, text_content=None, text_color=None):
        """
        Aggiorna le proprietà visive di una specifica cella esistente.

        Args:
            r (int): Indice riga.
            c (int): Indice colonna.
            color (QColor): Nuovo colore di sfondo (se None, non cambia).
            text_content (str, optional): Nuovo testo da mostrare (se None, non cambia).
            text_color (QColor, optional): Nuovo colore del testo.
        """
        if not (0 <= r < self.map_size and 0 <= c < self.map_size): return

        # Aggiorna il colore della cella
        if color is not None:
            if self.rects[r][c].brush().color() != color: # Evita repaint inutili
                self.rects[r][c].setBrush(QBrush(color))

        # Aggiorna l'etichetta della cella
        if text_content is not None:
            item = self.texts[r][c]
            # Ricalcola la posizione solo se il testo cambia
            if item.toPlainText() != str(text_content):
                item.setPlainText(str(text_content))
                dx = (self.cell_size - item.boundingRect().width()) / 2
                dy = (self.cell_size - item.boundingRect().height()) / 2
                item.setPos((c * self.cell_size) + dx, (r * self.cell_size) + dy)
        
        if text_color is not None:
            self.texts[r][c].setDefaultTextColor(text_color)
