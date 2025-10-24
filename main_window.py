# main_window.py
# This file defines the main application window and all its UI elements.

import numpy as np
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QSlider, QLabel, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont # ## MODERN UI ## Import QFont for custom fonts

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Import our signal generation function from the other file.
from signal_logic import generate_signal_data

class MainWindow(QMainWindow):
    """ Main application window class. """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signal Explorer")
        self.setGeometry(100, 100, 1200, 800) # Increased width for the sidebar

        # --- Core Signal Parameters ---
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
        """ Creates and arranges all the UI widgets with a modern layout. """
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # ## MODERN UI ## Main layout is now HORIZONTAL to accommodate a sidebar.
        main_layout = QHBoxLayout(main_widget)

        # --- Plot Layout (Left Side) ---
        plot_layout = QVBoxLayout()
        
        self.time_figure = Figure(figsize=(10, 3))
        self.time_canvas = FigureCanvas(self.time_figure)
        self.ax_time = self.time_figure.add_subplot(111)

        self.freq_figure = Figure(figsize=(10, 3))
        self.freq_canvas = FigureCanvas(self.freq_figure)
        self.ax_freq = self.freq_figure.add_subplot(111)

        plot_layout.addWidget(self.time_canvas)
        plot_layout.addWidget(self.freq_canvas)

        # --- Controls Panel (Right Side) ---
        # ## MODERN UI ## Create a dedicated vertical layout for controls.
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(20) # Add nice spacing between control groups

        # Amplitude Controls
        self.amp_value_label = QLabel("Amplitude: 5.0") # Interactive value label
        self.amp_slider = QSlider(Qt.Orientation.Horizontal); self.amp_slider.setRange(1, 100); self.amp_slider.setValue(50)
        controls_layout.addWidget(self.amp_value_label)
        controls_layout.addWidget(self.amp_slider)

        # Frequency Controls
        self.freq_value_label = QLabel("Frequency: 5 Hz")
        self.freq_slider = QSlider(Qt.Orientation.Horizontal); self.freq_slider.setRange(1, 100); self.freq_slider.setValue(5)
        controls_layout.addWidget(self.freq_value_label)
        controls_layout.addWidget(self.freq_slider)
        
        # Phase Controls
        self.phase_value_label = QLabel("Phase: 0°")
        self.phase_slider = QSlider(Qt.Orientation.Horizontal); self.phase_slider.setRange(0, 360); self.phase_slider.setValue(0)
        controls_layout.addWidget(self.phase_value_label)
        controls_layout.addWidget(self.phase_slider)
        
        controls_layout.addStretch() # Pushes controls to the top

        # Create a container widget for the controls to style them nicely.
        controls_container = QWidget()
        controls_container.setLayout(controls_layout)
        controls_container.setFixedWidth(250) # Give the sidebar a fixed width

        # --- Assemble Main Layout ---
        main_layout.addLayout(plot_layout)
        main_layout.addWidget(controls_container)

        # Apply the global dark theme and styles.
        self._apply_styles()

    def _connect_signals(self):
        """ Connects widget signals (e.g., slider moved) to slots (functions). """
        self.amp_slider.valueChanged.connect(self.update_plots)
        self.freq_slider.valueChanged.connect(self.update_plots)
        self.phase_slider.valueChanged.connect(self.update_plots)

    def update_plots(self):
        """ This function is called whenever a slider value changes. """
        # Get values and update value labels
        amplitude = self.amp_slider.value() / 10.0
        self.amp_value_label.setText(f"Amplitude: {amplitude:.1f}")
        
        frequency = self.freq_slider.value()
        self.freq_value_label.setText(f"Frequency: {frequency} Hz")

        phase_deg = self.phase_slider.value()
        self.phase_value_label.setText(f"Phase: {phase_deg}°")

        # Call the external logic function to do the math.
        data = generate_signal_data(
            amplitude=amplitude,
            frequency=frequency,
            phase_deg=phase_deg,
            time_vector=self.t,
            sampling_freq=self.sampling_frequency
        )

        # Update the plots with the data returned by the logic function.
        self._update_time_plot(data["time_signal"])
        self._update_freq_plot(data["freq_axis"], data["freq_magnitude"])

    def _update_time_plot(self, time_signal):
        """ Redraws the time domain plot. """
        self.ax_time.clear()
        self.ax_time.plot(self.t, time_signal, color='#00AEEF', linewidth=2) # Thicker line
        self.ax_time.set_title("Time Domain", color="#FFFFFF")
        self.ax_time.set_xlabel("Time (s)", color="#FFFFFF"); self.ax_time.set_ylabel("Amplitude", color="#FFFFFF")
        self.ax_time.set_xlim(0, 0.5); self.ax_time.set_ylim(-11, 11)
        self.ax_time.grid(True, linestyle='--', color='#FFFFFF', alpha=0.15) # Fainter grid
        self.time_canvas.draw()

    def _update_freq_plot(self, freq_axis, freq_magnitude):
        """ Redraws the frequency domain plot. """
        self.ax_freq.clear()
        markerline, stemlines, baseline = self.ax_freq.stem(
            freq_axis, freq_magnitude, linefmt='#00AEEF', markerfmt="o", basefmt=" "
        )
        markerline.set_markerfacecolor('#00AEEF')
        markerline.set_markeredgecolor('#00AEEF')
        markerline.set_markersize(5)
        self.ax_freq.set_title("Frequency Domain (FFT)", color="#FFFFFF")
        self.ax_freq.set_xlabel("Frequency (Hz)", color="#FFFFFF"); self.ax_freq.set_ylabel("Magnitude", color="#FFFFFF")
        self.ax_freq.set_xlim(0, 120); self.ax_freq.set_ylim(0, 11)
        self.ax_freq.grid(True, linestyle='--', color='#FFFFFF', alpha=0.15)
        self.freq_canvas.draw()

    def _apply_styles(self):
        """ Applies a dark theme and custom styles to the app and plots. """
        # ## MODERN UI ## Use a modern sans-serif font
        self.setFont(QFont("Segoe UI", 10)) 
        
        self.setStyleSheet("""
            QMainWindow { background-color: #1E1E1E; }
            QWidget { background-color: #1E1E1E; color: #E0E0E0; }
            QLabel { font-weight: bold; font-size: 14px; }
            QSlider::groove:horizontal { border: 1px solid #444; height: 4px; background: #393939; border-radius: 2px; }
            QSlider::handle:horizontal { background-color: #00AEEF; border: 1px solid #00AEEF; width: 18px; margin: -8px 0; border-radius: 9px; }
        """)
        
        # ## MODERN UI ## This is the crucial fix for the plot text color.
        # This loop styles both plots consistently.
        for ax in [self.ax_time, self.ax_freq]:
            ax.figure.set_facecolor('#1E1E1E')
            ax.set_facecolor('#1E1E1E')
            
            # Set color for all text elements
            ax.title.set_color('white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            
            # Set color for plot borders (spines)
            ax.spines['left'].set_color('white')
            ax.spines['bottom'].set_color('white')
            # Hide the top and right borders for a cleaner look
            ax.spines['top'].set_color('#1E1E1E')
            ax.spines['right'].set_color('#1E1E1E')
