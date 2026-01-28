from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QSpinBox, QLabel, QStyle)
from PyQt6.QtCore import QTimer, Qt
import numpy as np
from typing import List, Dict, Tuple, Union, Optional

from .config import settings
from .IO_saver.io_manager import ImageExporter
from .components.path_renderer import PathRenderer
from .components.heatmap_renderer import HeatmapScene
from .components.zoomable_view import ZoomableView

class VisualizerWindow(QWidget):
    """
    Finestra principale (GUI) per la visualizzazione dei percorsi e delle heatmap.

    Gestisce l'animazione frame-by-frame, la sincronizzazione tra le viste 
    (Path e Heatmap), i controlli utente (Play/Pause, Slider) e l'esportazione
    delle immagini su disco.

    Attributes:
        raw_map (List[List[int]]): La griglia statica che rappresenta l'ambiente.
        path_coords (List[Tuple[int, int]]): La lista sequenziale di coordinate del percorso.
        matrix_list (List[np.ndarray]): Lista opzionale di matrici per la heatmap dinamica.
        coord_to_alias (Dict): Mapping per convertire coordinate (r,c) in etichette leggibili.
        save_render (bool): Flag per abilitare il salvataggio automatico dei frame renderizzati.
    """

    def __init__(self, 
                 raw_map: List[List[int]], 
                 path: List[Union[Tuple[int, int], str, int]], 
                 format_mapping_map: Dict[Tuple[int, int], str], 
                 delay: int, 
                 matrix_list: Optional[List[np.ndarray]] = None,
                 save_render: bool = False):
        """
        Inizializza la finestra di visualizzazione, valida i dati e prepara le scene.

        Args:
            raw_map (List[List[int]]): Matrice bidimensionale rappresentante la mappa (0=libero, 1=ostacolo).
            path (List[Union[Tuple, str]]): Lista di passi del percorso. Può contenere coordinate 
                (r, c) o alias (stringhe/ID) definiti in `format_mapping_map`.
            format_mapping_map (Dict): Dizionario {Coordinate: Alias} per la visualizzazione.
            delay (int): Ritardo in millisecondi tra i frame dell'animazione.
            matrix_list (List, optional): Lista di matrici numeriche per generare la heatmap 
                frame per frame. Default è None.
            save_render (bool, optional): Se True, salva ogni frame visualizzato come immagine PNG. 
                Default è False.

        Raises:
            ValueError: Se la mappa è vuota, irregolare o se il path contiene dati non validi/fuori limiti.
        """
        super().__init__()

        if not raw_map or not raw_map[0]:
            raise ValueError("Errore: 'raw_map' è vuota o non valida.")
        
        self.rows = len(raw_map)
        self.cols = len(raw_map[0])
        
        # Verifica consistenza geometrica (deve essere quadrata)
        if any(len(row) != self.cols for row in raw_map):
            raise ValueError("Errore: 'raw_map' deve essere una matrice quadrata.")

        self.raw_map = raw_map
        self.map_size = len(self.raw_map) 
        
        if not format_mapping_map:
            raise ValueError("Errore: 'format_mapping_map' è obbligatorio.")
            
        self.coord_to_alias = format_mapping_map
        self.alias_to_coord = {v: k for k, v in format_mapping_map.items()}

        # Converte tutto in formato canonico (r, c)
        self.path_coords = self._validate_and_convert_path(path)
        self.matrix_list = matrix_list if matrix_list else []
        
        self.total_frames = max(len(self.path_coords), len(self.matrix_list))
        self.current_frame = 0
        self.is_playing = False
        self.delay = delay
        
        self.save_render = save_render
        self.exporter = ImageExporter()
        self.saved_frames = set() 
        
        self._init_ui()
        self._setup_scenes()
        
        # Timer per il loop di animazione
        self.anim_timer = QTimer(self)
        self.anim_timer.setInterval(self.delay)
        self.anim_timer.timeout.connect(self._advance_frame)

        # Rendering iniziale (Frame 0)
        self.set_frame(0)

    def _validate_and_convert_path(self, path: List) -> List[Tuple[int, int]]:
        """
        Normalizza il path di input convertendo eventuali alias in coordinate (r, c).

        Gestisce polimorfismo nell'input:
        1. Se sono coordinate: verifica i limiti della mappa.
        2. Se sono alias: cerca la corrispondenza nel mapping inverso.

        Args:
            path (List): Il path grezzo in input.

        Returns:
            List[Tuple[int, int]]: Lista pulita di coordinate tuple (row, col).

        Raises:
            ValueError: Se un punto è fuori mappa o un alias è sconosciuto.
        """
        if not path:
            return []
        converted_path = []
        first_elem = path[0]

        # Rilevamento tipo: Coordinate (Tuple/List/Array) vs Alias (Str/Int scalare)
        if isinstance(first_elem, (list, tuple, np.ndarray)):
            for idx, point in enumerate(path):
                if len(point) != 2:
                    raise ValueError(f"Errore path indice {idx}: {point} non valido.")
                r, c = point
                # Boundary Check 
                if not (0 <= r < self.rows and 0 <= c < self.cols):
                    raise ValueError(f"Errore path: {point} fuori limiti.")
                converted_path.append((int(r), int(c)))
        else:
            # Gestione Alias
            for idx, alias in enumerate(path):
                if alias not in self.alias_to_coord:
                    raise ValueError(f"Errore path indice {idx}: Alias '{alias}' non trovato.")
                converted_path.append(self.alias_to_coord[alias])

        return converted_path

    def _init_ui(self):
        """Configura il layout principale, le dimensioni della finestra e lo stile globale."""
        self.setWindowTitle(settings.WINDOW_TITLE)
        self.setGeometry(100, 100, *settings.WINDOW_SIZE)
        self.setStyleSheet(f"background-color: {settings.BG_COLOR_UI}; color: white;")
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(self._create_views())
        main_layout.addLayout(self._create_controls())
        self.setLayout(main_layout)

    def _create_views(self) -> QHBoxLayout:
        """
        Crea e dispone le viste grafiche (Scene) all'interno di wrapper zoomabili.
        
        Returns:
            QHBoxLayout: Il layout orizzontale contenente le viste.
        """
        layout = QHBoxLayout()
        
        def create_view(scene):
            return ZoomableView(scene)

        # Vista Percorso
        self.path_scene = PathRenderer(self.raw_map)
        self.path_view = create_view(self.path_scene)
        layout.addWidget(self.path_view)

        # Vista Heatmap
        if self.matrix_list:
            self.heat_scene = HeatmapScene(self.raw_map)
            self.heat_view = create_view(self.heat_scene)
            layout.addWidget(self.heat_view)
            
        return layout

    def _create_controls(self) -> QHBoxLayout:
        """
        Genera i widget di controllo (Play, Slider, Spinbox) e i relativi segnali.

        Returns:
            QHBoxLayout: Il layout contenente i controlli.
        """
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 10, 20, 10)

        # Bottone Play/Pause
        self.btn_play = QPushButton()
        self.btn_play.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.btn_play.clicked.connect(self._toggle_play)
        self.btn_play.setStyleSheet("padding: 5px; background-color: #34495e; border-radius: 5px;")
        
        # Slider di navigazione temporale
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, max(0, self.total_frames - 1))
        self.slider.valueChanged.connect(self._on_slider_change)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal { height: 8px; background: #bdc3c7; border-radius: 4px; }
            QSlider::handle:horizontal { background: #1abc9c; width: 16px; margin: -4px 0; border-radius: 8px; }
        """)

        # Input numerico diretto
        self.spinbox = QSpinBox()
        self.spinbox.setRange(0, max(0, self.total_frames - 1))
        self.spinbox.valueChanged.connect(self._on_spinbox_change)
        self.spinbox.setStyleSheet("color: black; padding: 5px; font-weight: bold;")
        
        # Etichetta conteggio
        lbl_total = QLabel(f"/ {max(0, self.total_frames - 1)}")
        lbl_total.setStyleSheet("font-weight: bold; margin-left: 5px;")
        

        layout.addWidget(self.btn_play)
        layout.addWidget(self.slider)
        layout.addWidget(self.spinbox)
        layout.addWidget(lbl_total)
        
        return layout
    
    def _get_cell_label(self, coord: Tuple[int, int]) -> str:
        """
        Recupera in sicurezza l'etichetta (alias) per una data coordinata.
        """
        try:
            key = (int(coord[0]), int(coord[1]))
            return str(self.coord_to_alias.get(key, "")) 
        except (ValueError, TypeError, IndexError):
            # Fallback in caso di coordinate malformate
            return str(coord)

    def _setup_scenes(self):
        """Inizializza il disegno statico delle griglie nelle scene."""
        # Funzione lambda per passare il metodo di lookup alla scena grafica
        mapper = lambda c: self._get_cell_label(c)
        
        if self.path_coords:
            start_coord = self.path_coords[0]
            goal_coord = self.path_coords[-1]
        else:
            start_coord = (0,0)
            goal_coord = (0,0)
        
        self.path_scene.draw_initial_grid(start_coord, goal_coord, mapper)

    # --- LOGICA DI CONTROLLO ---

    def _toggle_play(self):
        """Gestisce l'alternanza tra stato Play e Pause dell'animazione."""
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.btn_play.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
            self.anim_timer.start()
        else:
            self.btn_play.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
            self.anim_timer.stop()

    def _advance_frame(self):
        """Slot chiamato dal QTimer: avanza di un frame se possibile."""
        if self.current_frame < self.total_frames - 1:
            self.set_frame(self.current_frame + 1)
        else:
            # Fine animazione: stop timer e reset icona
            self.is_playing = False
            self.anim_timer.stop()
            self.btn_play.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))

    def _on_slider_change(self, val):
        """Slot per movimento manuale dello slider."""
        self.set_frame(val)

    def _on_spinbox_change(self, val):
        """Slot per cambio valore numerico diretto."""
        self.set_frame(val)

    def set_frame(self, frame_idx: int):
        """
        Imposta lo stato dell'applicazione a uno specifico frame temporale.

        Aggiorna slider, spinbox, scene grafiche e gestisce l'export su disco.

        Args:
            frame_idx (int): L'indice del frame da visualizzare (0-based).
        """
        if self.total_frames == 0: return

        frame_idx = max(0, min(frame_idx, self.total_frames - 1))
        self.current_frame = frame_idx
        
        # IMPORTANTE: Blocchiamo i segnali per evitare loop ricorsivi
        self.slider.blockSignals(True)
        self.spinbox.blockSignals(True)
        self.slider.setValue(frame_idx)
        self.spinbox.setValue(frame_idx)
        self.slider.blockSignals(False)
        self.spinbox.blockSignals(False)

        # Aggiorna Path
        self.path_scene.update_state(self.path_coords, frame_idx)

        # Aggiorna Heatmap
        if self.matrix_list:
            heat_idx = min(frame_idx, len(self.matrix_list) - 1)
            mapper = lambda c: self._get_cell_label(c)
            self.heat_scene.draw_matrix(self.matrix_list[heat_idx], mapper)
            
        # Esportazione Immagini
        if self.save_render and frame_idx not in self.saved_frames:
            try:
                cell_size = settings.CELL_SIZE
                
                # Salva Path Map
                self.exporter.save_snapshot(
                    scene=self.path_scene,
                    file_prefix="path_animation",
                    index=frame_idx,
                    map_size=self.map_size,
                    cell_size=cell_size
                )
                
                # Salva Heatmap (se esiste)
                if self.matrix_list:
                    self.exporter.save_snapshot(
                        scene=self.heat_scene,
                        file_prefix="heatmap_animation",
                        index=frame_idx,
                        map_size=self.map_size,
                        cell_size=cell_size
                    )
                
                # Segna come salvato per evitare duplicati
                self.saved_frames.add(frame_idx)
                
            except Exception as e:
                # Logghiamo l'errore in console senza bloccare la GUI
                print(f"Errore durante il salvataggio del frame {frame_idx}: {e}")