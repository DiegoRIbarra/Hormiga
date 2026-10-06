import sys
import os
import random
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
                             QGridLayout, QVBoxLayout, QHBoxLayout, 
                             QFrame)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget 
from PySide6.QtGui import QBrush, QColor, QFont, QPen, QPixmap, QDrag
from PySide6.QtCore import Qt, QTimer, QPointF, QUrl, QRectF, QMimeData
from bfs_logic import bfs_shortest_path

# Constantes de Diseño
TILED_SIZE = 50
COLOR_BG = '#0b0d17'

class Tablero(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hormiga BFS Visualizer")
        self.setFixedSize(950, 600)
        self.setStyleSheet(f"background-color: {COLOR_BG};")

        # Estado del juego
        self.grid = [[0 for _ in range(8)] for _ in range(10)]
        self.ant_pos = (0, 0)
        self.food_pos = (9, 7)
        
        self.initUI()

    def initUI(self):
        self.main_layout = QHBoxLayout(self)
        
        # --- PANEL IZQUIERDO (Tablero) ---
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout(self.left_panel)
        
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(5)
        self.cells = {}

        for r in range(10):
            for c in range(8):
                cell = QFrame()
                cell.setFixedSize(TILED_SIZE, TILED_SIZE)
                cell.setStyleSheet("background-color: #1a1d2e; border: 1px solid #333; border-radius: 5px;")
                self.grid_layout.addWidget(cell, r, c)
                self.cells[(r, c)] = cell

        self.left_layout.addWidget(self.grid_container)
        
        # Fila de Botones
        self.btn_row = QHBoxLayout()
        
        self.reset_btn = QPushButton("Reiniciar 🍎")
        self.reset_btn.setStyleSheet("background-color: #444; color: white; padding: 10px; border-radius: 5px;")
        self.reset_btn.clicked.connect(self.reset_game)
        
        self.start_btn = QPushButton("Iniciar Hormiga 🐜")
        self.start_btn.setStyleSheet("background-color: #2ecc71; color: white; padding: 10px; border-radius: 5px; font-weight: bold;")
        self.start_btn.clicked.connect(self.start_bfs)
        
        self.btn_row.addWidget(self.reset_btn)
        self.btn_row.addWidget(self.start_btn)
        self.left_layout.addLayout(self.btn_row)

        # --- PANEL DERECHO (Video) ---
        self.right_panel = QWidget()
        self.right_panel.setFixedWidth(400)
        self.right_layout = QVBoxLayout(self.right_panel)

        self.video_widget = QVideoWidget()
        self.video_widget.setStyleSheet("background-color: black;")
        
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.video_widget)

        video_path = os.path.abspath(os.path.join("datos base", "Subway Surfers (2026) - Gameplay [4K 16x9] No Copyright.mp4"))
        self.player.setSource(QUrl.fromLocalFile(video_path))
        self.player.setLoops(QMediaPlayer.Infinite)
        self.player.play()

        self.right_layout.addWidget(self.video_widget)

        # Botón Flotante (Cerrar/Abrir Video)
        self.float_btn = QPushButton("✖", self)
        self.float_btn.setFixedSize(40, 40)
        self.float_btn.move(900, 10)
        self.float_btn.setStyleSheet("background-color: red; color: white; font-weight: bold; border-radius: 20px;")
        self.float_btn.clicked.connect(self.toggle_video)
        self.float_btn.raise_() # <--- ESTO LO PONE AL FRENTE

        self.main_layout.addWidget(self.left_panel)
        self.main_layout.addWidget(self.right_panel)

        # Elementos Visuales (Símbolos)
        self.hormiga_label = QLabel('🐜')
        self.hormiga_label.setFixedSize(TILED_SIZE, TILED_SIZE)
        self.hormiga_label.setAlignment(Qt.AlignCenter)
        self.hormiga_label.setStyleSheet("background: transparent; font-size: 25px;")
        self.hormiga_label.setParent(self)
        
        self.comida_label = QLabel('🍎')
        self.comida_label.setFixedSize(TILED_SIZE, TILED_SIZE)
        self.comida_label.setAlignment(Qt.AlignCenter)
        self.comida_label.setStyleSheet("background: transparent; font-size: 25px;")
        self.comida_label.setParent(self)

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_step)

        self.reset_game()

    def toggle_video(self):
        if self.right_panel.isVisible():
            self.right_panel.hide()
            self.float_btn.setText("▶")
            self.float_btn.setStyleSheet("background-color: green; color: white; border-radius: 20px;")
            self.setFixedWidth(500)
            self.float_btn.move(450, 10)
        else:
            self.right_panel.show()
            self.float_btn.setText("✖")
            self.float_btn.setStyleSheet("background-color: red; color: white; border-radius: 20px;")
            self.setFixedWidth(950)
            self.float_btn.move(900, 10)
        self.float_btn.raise_()

    def reset_game(self):
        self.food_pos = (random.randint(0, 9), random.randint(0, 7))
        self.ant_pos = (0, 0)
        self.timer.stop()
        self.update_visuals()

    def update_visuals(self):
        # Obtenemos la posición del tablero para centrar la hormiga y la manzana
        grid_pos = self.grid_container.pos()
        
        self.hormiga_label.move(
            grid_pos.x() + self.ant_pos[1] * TILED_SIZE + 5, 
            grid_pos.y() + self.ant_pos[0] * TILED_SIZE + 5
        )
        self.comida_label.move(
            grid_pos.x() + self.food_pos[1] * TILED_SIZE + 5, 
            grid_pos.y() + self.food_pos[0] * TILED_SIZE + 5
        )

    def start_bfs(self):
        path = bfs_shortest_path(self.grid, self.ant_pos, self.food_pos)
        if path:
            self.current_path = path
            self.path_index = 1
            self.timer.start(200)
        else:
            print("No se encontró camino")

    def animate_step(self):
        if hasattr(self, 'current_path') and self.path_index < len(self.current_path):
            self.ant_pos = self.current_path[self.path_index]
            self.path_index += 1
            self.update_visuals()
        else:
            self.timer.stop()
            # Al llegar a la comida, reinicia la manzana
            self.reset_game()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Tablero()
    window.show()
    sys.exit(app.exec())
