import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, fft

# Signal parameters
a = 0       # Mean value
b = 10      # Standard deviation
n = 500     # Number of points
Fs = 1000   # Sampling frequency (Hz)
F_max = 25  # Maximum signal frequency (Hz)

# Generate a random signal
signal_data = np.random.normal(a, b, n)

# Time scale
time_values = np.arange(n) / Fs

# Normalize frequency (calculation for Butterworth LPF)
w = F_max / (Fs / 2)
sos = signal.butter(3, w, 'low', output='sos')

# Bidirectional filtering (avoiding phase shift)
filtered_signal = signal.sosfiltfilt(sos, signal_data)

# Function for plotting and saving graphs
def plot_signal(x, y, title, xlabel, ylabel, filename):
    save_dir = "./figures"
    os.makedirs(save_dir, exist_ok=True)
    save_path = f"{save_dir}/{filename}.png"

    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))  # 21 cm × 14 cm
    ax.plot(x, y, linewidth=1, color='tab:blue')

    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    plt.title(title, fontsize=14)

    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

    # Save the image with improved parameters
    fig.savefig(save_path, dpi=600, bbox_inches='tight', transparent=True)

    plt.show()


# Plot the filtered signal
plot_signal(time_values, filtered_signal,
            "Сигнал з максимальною частотою F_max = 25 Гц",
            "Час (секунди)",
            "Амплітуда сигналу",
            "filtered_signal")

# Compute and plot the signal spectrum
spectrum = fft.fft(filtered_signal)
spectrum_magnitude = np.abs(fft.fftshift(spectrum))  # Magnitude of the amplitude spectrum
freq_values = fft.fftshift(fft.fftfreq(n, 1 / Fs))  # Scaled frequency values

#  Plot the spectrum
plot_signal(freq_values, spectrum_magnitude,
            "Спектр сигналу з максимальною частотою F_max = 25 Гц",
            "Частота (Гц)",
            "Амплітуда спектра",
            "signal_spectrum")
