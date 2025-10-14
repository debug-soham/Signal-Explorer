# main_window.py
# This file defines the main application window and all its UI elements.

import numpy as np
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QSlider, QLabel)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Import our signal generation function from the other file.
from signal_logic import generate_signal_data

class MainWindow(QMainWindow):
    """ Main application window class. """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signal Explorer")
        self.setGeometry(100, 100, 1000, 800)

        # --- Core Signal Parameters ---
        # These define the base properties of our signal.
        self.sampling_frequency = 500
        self.time_duration = 2
        self.t = np.linspace(0, self.time_duration, self.sampling_frequency * self.time_duration, endpoint=False)
        
        # Build the user interface.
        self._setup_ui()
        
        # Connect UI elements (like sliders) to functions.
        self._connect_signals()

        # Perform an initial plot update to show a default signal.
        self.update_plots()

    def _setup_ui(self):
        """ Creates and arranges all the UI widgets. """
        # A central widget holds all other UI components.
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # The main layout arranges widgets vertically.
        main_layout = QVBoxLayout(main_widget)

        # --- Create Plots ---
        self.time_figure = Figure(figsize=(10, 3))
        self.time_canvas = FigureCanvas(self.time_figure)
        self.ax_time = self.time_figure.add_subplot(111)

        self.freq_figure = Figure(figsize=(10, 3))
        self.freq_canvas = FigureCanvas(self.freq_figure)
        self.ax_freq = self.freq_figure.add_subplot(111)

        # Add plots to the main layout.
        main_layout.addWidget(self.time_canvas)
        main_layout.addWidget(self.freq_canvas)

        # --- Create Controls ---
        # A horizontal layout for the sliders and their labels.
        controls_layout = QHBoxLayout()
        
        amp_label = QLabel("Amplitude:")
        self.amp_slider = QSlider(Qt.Orientation.Horizontal); self.amp_slider.setRange(1, 100); self.amp_slider.setValue(50)
        
        freq_label = QLabel("Frequency (Hz):")
        self.freq_slider = QSlider(Qt.Orientation.Horizontal); self.freq_slider.setRange(1, 100); self.freq_slider.setValue(5)
        
        phase_label = QLabel("Phase (degrees):")
        self.phase_slider = QSlider(Qt.Orientation.Horizontal); self.phase_slider.setRange(0, 360); self.phase_slider.setValue(0)
        
        # Add controls to their own layout.
        controls_layout.addWidget(amp_label); controls_layout.addWidget(self.amp_slider)
        controls_layout.addWidget(freq_label); controls_layout.addWidget(self.freq_slider)
        controls_layout.addWidget(phase_label); controls_layout.addWidget(self.phase_slider)
        
        # Add the entire controls layout to the main layout.
        main_layout.addLayout(controls_layout)

        # Apply the dark theme styling.
        self._apply_styles()

    def _connect_signals(self):
        """ Connects widget signals (e.g., slider moved) to slots (functions). """
        self.amp_slider.valueChanged.connect(self.update_plots)
        self.freq_slider.valueChanged.connect(self.update_plots)
        self.phase_slider.valueChanged.connect(self.update_plots)

    def update_plots(self):
        """ This function is called whenever a slider value changes. """
        # 1. Get current values from the UI sliders.
        amplitude = self.amp_slider.value() / 10.0
        frequency = self.freq_slider.value()
        phase_deg = self.phase_slider.value()

        # 2. Call the external logic function to do the math.
        data = generate_signal_data(
            amplitude=amplitude,
            frequency=frequency,
            phase_deg=phase_deg,
            time_vector=self.t,
            sampling_freq=self.sampling_frequency
        )

        # 3. Update the plots with the data returned by the logic function.
        self._update_time_plot(data["time_signal"])
        self._update_freq_plot(data["freq_axis"], data["freq_magnitude"])

    def _update_time_plot(self, time_signal):
        """ Redraws the time domain plot. """
        self.ax_time.clear()
        self.ax_time.plot(self.t, time_signal, color='cyan')
        self.ax_time.set_title("Time Domain")
        self.ax_time.set_xlabel("Time (s)"); self.ax_time.set_ylabel("Amplitude")
        self.ax_time.set_xlim(0, 0.5); self.ax_time.set_ylim(-11, 11)
        self.ax_time.grid(True, linestyle='--', alpha=0.4)
        self.time_canvas.draw()

    def _update_freq_plot(self, freq_axis, freq_magnitude):
        """ Redraws the frequency domain plot. """
        self.ax_freq.clear()
        self.ax_freq.stem(freq_axis, freq_magnitude, 'cyan', markerfmt="oc", basefmt=" ")
        self.ax_freq.set_title("Frequency Domain (FFT)")
        self.ax_freq.set_xlabel("Frequency (Hz)"); self.ax_freq.set_ylabel("Magnitude")
        self.ax_freq.set_xlim(0, 120); self.ax_freq.set_ylim(0, 11)
        self.ax_freq.grid(True, linestyle='--', alpha=0.4)
        self.freq_canvas.draw()

    def _apply_styles(self):
        """ Applies a dark theme and custom styles to the app and plots. """
        self.setStyleSheet("""
            QWidget { background-color: #262626; color: #FFFFFF; font-size: 14px; }
            QSlider::groove:horizontal { border: 1px solid #444; height: 8px; background: #393939; border-radius: 4px; }
            QSlider::handle:horizontal { background-color: #00AEEF; border: 1px solid #00AEEF; width: 18px; margin: -5px 0; border-radius: 9px; }
            QLabel { font-weight: bold; }
        """)
        
        # Style the plots to match the dark theme
        for ax in [self.ax_time, self.ax_freq]:
            ax.figure.set_facecolor('#262626')
            ax.set_facecolor('#262626')
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            ax.spines['left'].set_color('white')
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('#262626')
            ax.spines['right'].set_color('#262626')
            ax.title.set_color('white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
