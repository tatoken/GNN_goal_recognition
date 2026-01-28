import numpy as np
from ..config import settings
from .base_grid import BaseGridScene
from PyQt6.QtGui import QColor

class HeatmapScene(BaseGridScene):
    """
    Scena specializzata per visualizzare matrici di dati come mappe di calore.
    """
    def draw_matrix(self, matrix, node_mapper):
        """
        Renderizza una matrice numerica applicando un gradiente di colore.

        Normalizza i valori della matrice rispetto al massimo valore presente
        per generare colori coerenti.

        Args:
            matrix (np.ndarray): Matrice 2D di valori numerici.
            node_mapper (Callable): Funzione per etichette celle.
        """
        # Se è la prima volta, crea gli oggetti
        if not self.is_initialized:
            self._init_grid_items()
            
        maxv = np.max(matrix)
        
        for r in range(self.map_size):
            for c in range(self.map_size):
                
                # Se è un muro lo coloriamo come tale
                if self.map_data[r][c] == 1:
                    self._update_cell(r, c, settings.qcolors["WALL"], "")
                    continue

                # Altrimenti calcolo il calore normalizzato [0.0 - 1.0]
                val = matrix[r][c]
                norm = val / maxv if maxv != 0 else 0.0
                col = self.get_heatmap_color(norm)
                
                try:
                    node_id = str(node_mapper([r,c]))
                except:
                    node_id = ""
                
                self._update_cell(r, c, col, node_id, settings.qcolors["TEXT_HL"])

    def get_heatmap_color(self,value: float) -> QColor:
        """Restituisce un colore interpolato basato su un valore 0.0 - 1.0"""
        v = max(0.0, min(1.0, value))
        if v < 0.5:
            ratio = v * 2
            r = int(15 + (180 - 15) * ratio)
            g = int(0 + (50 - 0) * ratio)
            b = int(40 + (80 - 40) * ratio)
        else:
            ratio = (v - 0.5) * 2
            r = int(180 + (250 - 180) * ratio)
            g = int(50 + (230 - 50) * ratio)
            b = int(80 + (80 - 80) * ratio)
        return QColor(r, g, b)