from PyQt6.QtWidgets import  QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel
from PyQt6.QtGui import QColor, QBrush, QFont, QPen
from PyQt6.QtCore import Qt, QTimer
import numpy as np

from Map_Manager.Map_graph_manager import Map_graph_manager

class PathVisualizer(QWidget):

    def __init__(self, map_graph_manager:Map_graph_manager, S, G, path, delay, matrix_list=None):
        super().__init__()
        self.map_graph_manager=map_graph_manager
        self.map= map_graph_manager.get_map().map_data
        self.map_size=len(self.map)

        self.matrix_list = matrix_list
        self.has_heatmap = matrix_list is not None

        # Converti source/dest da nodo a cella (r,c)
        self.S=map_graph_manager.node_id_to_coord(S)
        self.G=map_graph_manager.node_id_to_coord(G)

        self.path = path
        self.delay = delay
        self.cell_size = 50

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Path + Heatmap Visualizer")
        self.setGeometry(100, 100, 1200, 650)

        main_layout = QVBoxLayout()
        
        # --- BUTTONS ---
        btn_layout = QHBoxLayout()
        zoom_in_btn = QPushButton("Zoom In")
        zoom_out_btn = QPushButton("Zoom Out")
        forward_btn = QPushButton(">>")
        back_btn = QPushButton("<<")
        zoom_in_btn.clicked.connect(lambda: self.path_view.scale(1.2, 1.2))
        zoom_out_btn.clicked.connect(lambda: self.path_view.scale(0.8, 0.8))
        forward_btn.clicked.connect(self.compute_path)
        back_btn.clicked.connect(self.compute_path)
        btn_layout.addWidget(zoom_in_btn)
        btn_layout.addWidget(zoom_out_btn)
        btn_layout.addWidget(forward_btn)
        btn_layout.addWidget(back_btn)
        main_layout.addLayout(btn_layout)

        # --- TWO CANVAS SIDE BY SIDE ---
        map_layout = QHBoxLayout()

        # • PATH VIEW
        self.path_scene = QGraphicsScene()
        self.path_view = QGraphicsView(self.path_scene)
        self.path_view.setFixedSize(self.map_size*self.cell_size+2, self.map_size*self.cell_size+2)
        map_layout.addWidget(self.path_view)
        

        # • HEATMAP VIEW
        if self.has_heatmap:
            self.heat_scene = QGraphicsScene()
            self.heat_view = QGraphicsView(self.heat_scene)
            self.heat_view.setFixedSize(self.map_size*self.cell_size+2, self.map_size*self.cell_size+2)
            map_layout.addWidget(self.heat_view)

        main_layout.addLayout(map_layout)
        self.setLayout(main_layout)

        # Draw initial path grid
        self.draw_grid()

        # Start heatmap animation if exists
        if self.has_heatmap:
            self.current_matrix_index = 0
            self.heat_timer = QTimer(self)
            self.heat_timer.setInterval(self.delay)
            self.heat_timer.timeout.connect(self.draw_heatmap_frame)
            self.heat_timer.start()

    # -----------------------------------------------------
    # DRAW MAP + TEXT
    # -----------------------------------------------------
    def draw_grid(self):
        self.path_scene.clear()
        idx = 0
        for r in range(self.map_size):
            for c in range(self.map_size):
                x, y = c*self.cell_size, r*self.cell_size
                rect = QGraphicsRectItem(x, y, self.cell_size, self.cell_size)

                if idx == self.S:
                    rect.setBrush(QBrush(QColor(0,128,0)))
                    text = "S"
                elif idx == self.G:
                    rect.setBrush(QBrush(QColor(255,215,0)))
                    text = "G"
                elif self.map[r][c] == 1:
                    rect.setBrush(QBrush(QColor(80,80,80)))
                    text = ""
                else:
                    rect.setBrush(QBrush(QColor(210,210,210)))
                    text = str(self.map_graph_manager.coord_to_node_id([r,c]))

                rect.setPen(QPen(QColor(255,255,255), 1))
                self.path_scene.addItem(rect)

                if text:
                    t = QGraphicsTextItem(text)
                    t.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                    t.setPos(x + self.cell_size/2 - t.boundingRect().width()/2,
                             y + self.cell_size/2 - t.boundingRect().height()/2)
                    self.path_scene.addItem(t)

                idx += 1

    # -----------------------------------------------------
    # DRAW HEATMAP FRAME
    # -----------------------------------------------------
    def draw_heatmap_frame(self):
        if self.current_matrix_index >= len(self.matrix_list):
            self.heat_timer.stop()
            return
        
        mat = self.matrix_list[self.current_matrix_index]
        self.heat_scene.clear()

        maxv = np.max(mat)

        for r in range(self.map_size):
            for c in range(self.map_size):
                x, y = c*self.cell_size, r*self.cell_size
                v = mat[r][c] / maxv if maxv != 0 else 0.0

                # Colore super-sensibile al millesimo
                color = jet_color(v)

                rect = QGraphicsRectItem(x, y, self.cell_size, self.cell_size)
                rect.setBrush(QBrush(color) if self.map[r][c] == 0 else QBrush(QColor(70,70,70)))
                rect.setPen(QPen(QColor(255,255,255), 1))
                self.heat_scene.addItem(rect)

        self.current_matrix_index += 1

    # -----------------------------------------------------
    # PATH ANIMATION
    # -----------------------------------------------------
    def compute_path(self):
        self._path_index = 0
        self.timer = QTimer(self)
        self.timer.setInterval(self.delay)
        self.timer.timeout.connect(self.highlight_next)
        self.timer.start()

    def highlight_next(self):
        if self._path_index >= len(self.path):
            self.timer.stop()
            return

        node = self.path[self._path_index]
        r,c=self.map_graph_manager.node_id_to_coord(node)

        for item in self.path_scene.items():
            if isinstance(item, QGraphicsRectItem):
                if item.rect().x()==c*self.cell_size and item.rect().y()==r*self.cell_size:
                    item.setBrush(QBrush(QColor(30,144,255)))
                    break

        self._path_index += 1

def jet_color(v: float) -> QColor:
    """Gradiente continuo tipo 'jet', molto sensibile anche a variazioni piccolissime."""
    r = min(1.0, max(0.0, 1.5 - abs(4*v - 3)))
    g = min(1.0, max(0.0, 1.5 - abs(4*v - 2)))
    b = min(1.0, max(0.0, 1.5 - abs(4*v - 1)))
    return QColor(int(r*255), int(g*255), int(b*255))