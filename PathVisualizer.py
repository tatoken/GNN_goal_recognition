from PyQt6.QtWidgets import  QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtGui import QColor, QBrush, QFont,QPen
from PyQt6.QtCore import Qt,QTimer
import time

class PathVisualizer(QWidget):
    def __init__(self, size, M, S, G,path_list,delay):
        super().__init__()
        self.size = size
        self.M = M
        self.S = S
        self.G = G
        self.path_list=path_list
        self.delay=delay
        self.cell_size = 50
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Path Visualizer")
        self.setGeometry(100, 100, 800, 600)
        
        main_layout = QVBoxLayout()
        
        # Pulsanti zoom
        button_layout = QHBoxLayout()
        zoom_in_btn = QPushButton("Zoom In")
        zoom_out_btn = QPushButton("Zoom Out")
        start_btn = QPushButton("Start")
        zoom_in_btn.clicked.connect(self.zoom_in)
        zoom_out_btn.clicked.connect(self.zoom_out)
        start_btn.clicked.connect(self.compute_path)
        button_layout.addWidget(zoom_in_btn)
        button_layout.addWidget(zoom_out_btn)
        button_layout.addWidget(start_btn)
        main_layout.addLayout(button_layout)
        
        # QGraphicsView e Scene
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(self.view.renderHints())
        main_layout.addWidget(self.view)
        self.setLayout(main_layout)
        
        self.draw_grid()
    
    def draw_grid(self):
        self.scene.clear()
        i=0
        for r in range(self.size):
            for c in range(self.size):
                x = c * self.cell_size
                y = r * self.cell_size
                rect = QGraphicsRectItem(x, y, self.cell_size, self.cell_size)

                # Colori e testo

                if self.M[r][c] == 1:
                    rect.setBrush(QBrush(QColor(220, 20, 60)))  # rosso
                    text = QGraphicsTextItem(str(i))
                    text.setDefaultTextColor(Qt.GlobalColor.black)
                else:
                    rect.setBrush(QBrush(QColor(211, 211, 211)))  # grigio chiaro
                    text = QGraphicsTextItem(str(i))
                    text.setDefaultTextColor(Qt.GlobalColor.black)

                rect.setPen(QPen(Qt.GlobalColor.black, 1))
                self.scene.addItem(rect)

                if text is not None:
                    text.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                    text.setPos(
                        x + self.cell_size / 2 - text.boundingRect().width() / 2,
                        y + self.cell_size / 2 - text.boundingRect().height() / 2
                    )
                    self.scene.addItem(text)
                i+=1

        # Imposta dimensione scena
        self.scene.setSceneRect(0, 0, self.size * self.cell_size, self.size * self.cell_size)
        self.view.setBackgroundBrush(QBrush(Qt.GlobalColor.white))

    def compute_path(self):
        self._path_index = 0

        self._timer = QTimer(self)             
        self._timer.setInterval(self.delay)         
        self._timer.timeout.connect(self._highlight_next_cell)
        self._timer.start()

    def _highlight_next_cell(self):
        if self._path_index >= len(self.path_list):
            self._timer.stop()
            return

        cell = self.path_list[self._path_index]
        r = (cell // self.size)
        c = (cell % self.size)

        for item in self.scene.items():
            if isinstance(item, QGraphicsRectItem):
                rect = item.rect()
                if rect.x() == c * self.cell_size and rect.y() == r * self.cell_size:
                    item.setBrush(QBrush(QColor(30, 144, 255))) 
                    break

        self._path_index += 1

    
    def zoom_in(self):
        self.view.scale(1.2, 1.2) 
    
    def zoom_out(self):
        self.view.scale(0.8, 0.8) 