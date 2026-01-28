from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtGui import QPainter

class ZoomableView(QGraphicsView):
    """
    Widget grafico personalizzato che estende QGraphicsView per supportare navigazione interattiva.
    
    Implementa funzionalità native di panning (trascinamento) e zooming tramite 
    rotella del mouse, ottimizzato per il rendering di scene complesse.
    """

    def __init__(self, scene):
        """
        Inizializza la vista collegandola a una scena specifica.

        Configura le modalità di rendering per la massima qualità visiva (Antialiasing)
        e imposta le performance per la gestione di viewport dinamiche.

        Args:
            scene (QGraphicsScene): La scena grafica da visualizzare.
        """
        super().__init__(scene)
        # Attivazione Antialiasing per linee e testo più morbidi
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        self.setStyleSheet("background: transparent; border: none;")
        
        # Abilita il trascinamento (Pan) usando la "mano"
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        
        # MinimalViewportUpdate ridisegna solo le aree strettamente necessarie quando il contenuto cambia
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.MinimalViewportUpdate)

    def wheelEvent(self, event):
        """
        Intercetta l'evento della rotella del mouse per gestire lo zoom in/out.

        Applica un fattore di scala incrementale basato sulla direzione dello scroll.
        Non richiede il tasto Ctrl premuto (comportamento diretto).

        Args:
            event (QWheelEvent): L'evento di input generato dal mouse.
        """
        zoom_in_factor = 1.02
        zoom_out_factor = 1 / zoom_in_factor

        # Controlla la direzione dello scroll
        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor

        # Applica la trasformazione di scala alla matrice della vista
        self.scale(zoom_factor, zoom_factor)