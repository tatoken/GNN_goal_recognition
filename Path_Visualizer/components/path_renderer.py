from PyQt6.QtCore import Qt
from .base_grid import BaseGridScene
from ..config import settings

class PathRenderer(BaseGridScene):
    """
    Scena specializzata per la visualizzazione di percorsi (Pathfinding).
    
    Gestisce la distinzione visiva tra celle statiche (Muri, Start, Goal)
    e dinamiche (il percorso che avanza).
    """
    def draw_initial_grid(self, start_coord, goal_coord, node_mapper):
        """
        Imposta lo stato iniziale statico della mappa.

        Args:
            start_coord (Tuple[int, int]): Coordinate di partenza.
            goal_coord (Tuple[int, int]): Coordinate di arrivo.
            node_mapper (Callable): Funzione che mappa [r,c] -> Etichetta stringa.
        """
        self.start_coord = start_coord
        self.goal_coord = goal_coord
        self.node_mapper = node_mapper
        
        # Crea la griglia fisica se non esiste
        if not self.is_initialized:
            self._init_grid_items()

        # Imposta lo stato statico (Muri, Start, Goal, ID nodi)
        for r in range(self.map_size):
            for c in range(self.map_size):
                color = settings.qcolors["BG_EMPTY"]
                try:
                    txt = str(self.node_mapper([r,c]))
                except:
                    txt = ""
                txt_col = settings.qcolors["TEXT"]
    
                if r == self.start_coord[0] and c == self.start_coord[1]:
                    color = settings.qcolors["START"]; txt = "S"; txt_col = Qt.GlobalColor.white
                elif r == self.goal_coord[0] and c == self.goal_coord[1]:
                    color = settings.qcolors["GOAL"]; txt = "G"; txt_col = Qt.GlobalColor.white
                elif self.map_data[r][c] == 1:
                    color = settings.qcolors["WALL"]; txt = ""
                
                # Aggiorna
                self._update_cell(r, c, color, txt, txt_col)

    def update_state(self, path_list, current_frame):
        """
        Aggiorna la visualizzazione per mostrare il percorso fino al frame corrente.

        Args:
            path_list (List[Tuple]): La lista completa delle coordinate del percorso.
            current_frame (int): L'indice temporale corrente dell'animazione.
        """
        
        for r in range(self.map_size):
            for c in range(self.map_size):
                # Se è Start/Goal/Muro saltalo per preservare i punti fissi
                if (r,c) == self.start_coord or (r,c) == self.goal_coord or self.map_data[r][c] == 1:
                    continue
                
                # Resetta al colore base per cancellare la scia precedente (se si torna indietro)
                self._update_cell(r, c, settings.qcolors["BG_EMPTY"],None,settings.qcolors["TEXT"])

        # Disegna il path fino al frame corrente
        limit = min(current_frame + 1, len(path_list))
        for i in range(limit):
            r, c = path_list[i]
            
            # Start e Goal li scuriamo leggermente per indicare il passaggio
            if (r,c) == self.start_coord:
                self._update_cell(r, c, settings.qcolors["START"].darker(200))
            elif (r,c) == self.goal_coord:
                self._update_cell(r, c, settings.qcolors["GOAL"].darker(200))
            else:
                self._update_cell(r, c, settings.qcolors["PATH"], None, settings.qcolors["TEXT_HL"])
