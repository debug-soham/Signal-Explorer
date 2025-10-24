# signal_logic.py
# This file contains the core signal processing functions.

import numpy as np
from scipy import signal

def generate_signal_data(amplitude, frequency, phase_deg, time_vector, sampling_freq, waveform_type): # <-- NEW ARGUMENT
    """
    Calculates signal properties for both time and frequency domains.

    Args:
        amplitude (float): The peak amplitude of the sine wave.
        frequency (float): The frequency of the sine wave in Hz.
        phase_deg (float): The phase shift in degrees.
        time_vector (np.array): An array representing the time points.
        sampling_freq (float): The rate at which the signal was sampled.
        waveform_type (str): The type of wave to generate ("Sine", "Square", etc.)

    Returns:
        A dictionary containing the calculated signal data arrays.
    """
    
    # --- Time Domain Calculation ---
    # Convert phase from degrees to radians, as required by numpy's sin function.
    phase_rad = np.deg2rad(phase_deg)
    
    # Calculate the 't' argument for the wave functions, including phase
    t_with_phase = 2 * np.pi * frequency * time_vector + phase_rad

    # --- Generate the selected waveform ---
    if waveform_type == "Sine":
        time_signal = amplitude * np.sin(t_with_phase)
    elif waveform_type == "Square":
        # 'duty=0.5' creates a standard 50% duty cycle square wave
        time_signal = amplitude * signal.square(t_with_phase, duty=0.5)
    elif waveform_type == "Triangle":
        # 'width=0.5' on a sawtooth creates a triangle wave
        time_signal = amplitude * signal.sawtooth(t_with_phase, width=0.5)
    elif waveform_type == "Sawtooth":
        # 'width=1' (default) creates a standard sawtooth wave
        time_signal = amplitude * signal.sawtooth(t_with_phase, width=1)
    else:
        # Default case / fallback
        time_signal = amplitude * np.sin(t_with_phase)

    # --- Frequency Domain Calculation ---
    # The number of samples in our signal.
    N = len(time_signal)
    
    # Calculate the Fast Fourier Transform (FFT).
    fft_raw = np.fft.fft(time_signal)
    
    # Generate the frequency axis for the FFT plot.
    fft_freq_axis = np.fft.fftfreq(N, 1 / sampling_freq)
    
    # We only need to plot the positive frequencies (the first half of the FFT result).
    positive_freq_mask = fft_freq_axis >= 0
    
    # Calculate the magnitude of the FFT and normalize it by N.
    # The multiplication by 2 accounts for the energy in the negative frequencies.
    fft_magnitude = (2/N) * np.abs(fft_raw[positive_freq_mask])
    
    # Return all results neatly packaged in a dictionary.
    return {
        "time_signal": time_signal,
        "freq_axis": fft_freq_axis[positive_freq_mask],
        "freq_magnitude": fft_magnitude
    }
