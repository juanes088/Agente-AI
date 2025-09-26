import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QObject
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
import random
import math
from sistema_audio import hablar, escuchar
import cerebro_ia

class RealisticAudioVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.is_speaking = False
        self.animation_time = 0
        
        # Configuracion de barras para visualizacion
        self.num_bars = 15
        self.bar_heights = [0.0] * self.num_bars
        self.target_heights = [0.0] * self.num_bars
        self.bar_velocities = [0.0] * self.num_bars
        
        self.smoothing_factor = 0.85  # Suavizado de movimiento
        self.noise_intensity = 0.3    # Ruido para naturalidad
        self.decay_rate = 0.92        # Velocidad de bajada
        self.attack_rate = 0.15       # Velocidad de subida
        
        self.frequencies = [0.8, 1.2, 1.6, 2.1, 1.4, 2.3, 1.9, 1.1, 0.9, 2.7, 1.7, 2.0, 1.3, 2.5, 0.7]
        self.phase_offsets = [random.uniform(0, 2*math.pi) for _ in range(self.num_bars)]
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)

    def initUI(self):
        # Configura la ventana principal
        self.setWindowTitle('👾 Roberto')
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #0a0a0a;")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
    def update_animation(self):
        # Actualiza la animacion de las barras
        if self.is_speaking:
            self.animation_time += 0.016
            self.update_realistic_bars()
        else:
            self.update_idle_state()
        self.update()
        
    def update_realistic_bars(self):
        # Calcula alturas de barras con ondas y ruido
        for i in range(self.num_bars):
            base_wave = math.sin(self.animation_time * self.frequencies[i] + self.phase_offsets[i])
            secondary_wave = math.sin(self.animation_time * self.frequencies[i] * 1.7 + self.phase_offsets[i] * 0.3)
            noise = self.perlin_like_noise(self.animation_time + i * 0.5) * self.noise_intensity
            combined_signal = (base_wave * 0.6 + secondary_wave * 0.3 + noise * 0.4)
            target = abs(combined_signal) + 0.1
            target *= random.uniform(0.7, 1.3)
            
            self.target_heights[i] = target
            diff = self.target_heights[i] - self.bar_heights[i]
            
            if diff > 0:
                self.bar_heights[i] += diff * self.attack_rate
            else:
                self.bar_heights[i] += diff * (1 - self.decay_rate)
            
            self.bar_heights[i] = max(0.05, min(1.0, self.bar_heights[i]))
    
    def update_idle_state(self):
        # Animacion suave para estado de reposo
        for i in range(self.num_bars):
            idle_target = 0.15 + 0.05 * math.sin(self.animation_time * 0.5 + i * 0.3)
            self.bar_heights[i] = self.bar_heights[i] * 0.98 + idle_target * 0.02
    
    def perlin_like_noise(self, x):
        # Genera ruido suave para las barras
        octave1 = math.sin(x * 2.0) * 0.5
        octave2 = math.sin(x * 4.0) * 0.25
        octave3 = math.sin(x * 8.0) * 0.125
        return octave1 + octave2 + octave3

    def set_speaking_mode(self, speaking):
        # Cambia entre modo hablando y reposo
        self.is_speaking = speaking
        if speaking:
            self.timer.start(16)
            for i in range(len(self.phase_offsets)):
                if random.random() < 0.3:
                    self.phase_offsets[i] = random.uniform(0, 2*math.pi)
        else:
            pass

    def paintEvent(self, event):
        # Dibuja la interfaz grafica
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        center_x = width // 2
        center_y = height // 2
        
        painter.fillRect(0, 0, width, height, QColor(10, 10, 10))
        
        bar_width = 12
        spacing = 8
        total_width = self.num_bars * bar_width + (self.num_bars - 1) * spacing
        start_x = center_x - total_width // 2
        
        for i in range(self.num_bars):
            height_factor = self.bar_heights[i]
            bar_height = int(20 + height_factor * 150)
            x = start_x + i * (bar_width + spacing)
            y = center_y - bar_height // 2
            
            if self.is_speaking:
                intensity = int(height_factor * 255)
                if intensity < 128:
                    color = QColor(0, intensity * 2, intensity // 2)
                else:
                    excess = intensity - 128
                    color = QColor(excess, 255, 128 + excess // 2)
            else:
                color = QColor(0, 80, 20)
            
            glow_pen = QPen(color.lighter(150))
            glow_pen.setWidth(bar_width + 2)
            painter.setPen(glow_pen)
            painter.drawLine(x + bar_width//2, y, x + bar_width//2, y + bar_height)
            
            main_pen = QPen(color)
            main_pen.setWidth(bar_width)
            painter.setPen(main_pen)
            painter.drawLine(x + bar_width//2, y, x + bar_width//2, y + bar_height)
            
            if height_factor > 0.5:
                highlight_pen = QPen(QColor(255, 255, 255, 150))
                highlight_pen.setWidth(2)
                painter.setPen(highlight_pen)
                painter.drawLine(x + bar_width//2 - 1, y, x + bar_width//2 + 1, y)
        
        painter.setPen(QPen(QColor(0, 255, 100)))
        painter.drawText(15, 30, "🤖 ROBERTO")
        
        if self.is_speaking:
            alpha = int(150 + 100 * math.sin(self.animation_time * 3))
            painter.setPen(QPen(QColor(0, 255, 255, alpha)))
            painter.drawText(15, 55, "💬 Hablando...")
        else:
            painter.setPen(QPen(QColor(100, 100, 100)))
            painter.drawText(15, 55, "👂 Escuchando...")

class RobertoCommunicator(QObject):
    speaking_changed = pyqtSignal(bool)

def roberto_main(communicator):
    # Inicia el asistente y maneja el loop principal
    hablar("Soy Roberto, tu agente de inteligencia artificial", communicator)
    print("\n🤖 ROBERTO")
    print("💻 abre [sitio] | busca [algo] | cierra chrome")
    print("🗣️ 'quiero hablar roberto' para conversar")
    
    while True:
        comando = escuchar()
        if comando:
            if cerebro_ia.procesar_comando(comando, communicator):
                if not cerebro_ia.MODO_ROBERTO:
                    hablar("Algo mas", communicator)
            else:
                hablar("No entendi", communicator)

if __name__ == "__main__":
    # Inicia la aplicacion grafica y el hilo principal
    app = QApplication(sys.argv)
    visualizer = RealisticAudioVisualizer()
    visualizer.show()
    
    communicator = RobertoCommunicator()
    communicator.speaking_changed.connect(visualizer.set_speaking_mode)
    
    roberto_thread = threading.Thread(target=roberto_main, args=(communicator,), daemon=True)
    roberto_thread.start()
    
    print("🤖 Roberto - Agente IA")
    
    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("\n👋 Roberto desconectado")
        sys.exit(0)