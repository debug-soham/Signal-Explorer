# Signal Explorer

A desktop application built with PyQt6 and Matplotlib to visualize different waveforms in the time and frequency domains. This tool allows you to interactively adjust signal parameters and see how they affect the signal's shape and its corresponding Fast Fourier Transform (FFT).

## Features
* **Real-time Visualization:** See instant updates to the Time Domain and Frequency Domain plots as you adjust parameters.
* **Selectable Waveforms:** Choose from several fundamental waveforms:
    * Sine
    * Square
    * Triangle
    * Sawtooth
* **Interactive Controls:** Use sliders to modify the signal's:
    * Amplitude
    * Frequency
    * Phase

## Requirements
This project requires Python and the following libraries, which are listed in `requirements.txt`:

* `numpy`
* `PyQt6`
* `matplotlib`
* `scipy`

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/debug-soham/Signal-Explorer
    cd signal-explorer
    ```

2.  **(Recommended) Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Mac, use `source venv/bin/activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```
