import os
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import QRectF, Qt
from ..config import settings

class ImageExporter:
    """
    Gestisce l'esportazione di scene grafiche (QGraphicsScene) in file immagine su disco.
    
    Si occupa della creazione delle directory, del calcolo delle risoluzioni di output
    e del rendering off-screen tramite QPainter.
    """
    
    def __init__(self, output_dir: str = settings.OUTPUT_DIR):
        """
        Inizializza l'esportatore e prepara la cartella di destinazione.

        Args:
            output_dir (str, optional): Percorso della cartella di output. 
                Default preso da settings.OUTPUT_DIR.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_snapshot(self, scene: QGraphicsScene, file_prefix: str, index: int, 
                      map_size: int, cell_size: int, scale: float = settings.EXPORT_SCALE):
        """
        Cattura un'istantanea della scena e la salva come file PNG.

        Esegue un rendering "off-screen" su una QPixmap. Supporta il ridimensionamento
        (scaling) per ottenere esportazioni ad alta risoluzione indipendenti dalla vista a schermo.

        Args:
            scene (QGraphicsScene): La scena da renderizzare.
            file_prefix (str): Prefisso per il nome del file (es. 'heatmap').
            index (int): Indice progressivo del frame (utile per animazioni).
            map_size (int): Numero di celle per lato della mappa (assumendo mappa quadrata).
            cell_size (int): Dimensione in pixel di una singola cella base.
            scale (float, optional): Fattore di moltiplicazione per la risoluzione output.
                Default preso da settings.EXPORT_SCALE.
        """
        
        # Calcolo dimensioni reali della scena e dimensioni target dell'immagine
        scene_dim = map_size * cell_size
        img_dim = int(scene_dim * scale)
        
        # Creazione canvas trasparente
        image = QPixmap(img_dim, img_dim)
        image.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(image)
        # Hint essenziali per la qualità dell'immagine esportata (specialmente col ridimensionamento)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        source_rect = QRectF(0, 0, scene_dim, scene_dim)
        target_rect = QRectF(0, 0, img_dim, img_dim)
        
        # Rendering effettivo
        scene.render(painter, target=target_rect, source=source_rect)
        painter.end()
        
        # Costruzione percorso e salvataggio
        filename = os.path.join(self.output_dir, f"{file_prefix}_{index:03d}.png")
        image.save(filename)

    def save_legend(self, pixmap: QPixmap, name: str):
        """
        Salva un oggetto QPixmap (es. una legenda colori) su disco.

        Args:
            pixmap (QPixmap): L'immagine della legenda già renderizzata.
            name (str): Il nome identificativo per il file (es. 'heatmap_legend').
        """
        filename = os.path.join(self.output_dir, f"legend_{name}.png")
        pixmap.save(filename)