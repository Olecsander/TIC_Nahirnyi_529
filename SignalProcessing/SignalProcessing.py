import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfiltfilt
from scipy.fft import fft, fftshift, fftfreq

# Вхідні параметри
n = 500
Fs = 1000
F_max = 23
F_filter = 30
Dt_values = [2, 4, 8, 16]

time = np.arange(n) / Fs
signal = np.random.randn(n)

# Фільтрація вихідного сигналу
w = F_max / (Fs / 2)
filter_params = butter(3, w, 'low', output='sos')
filtered_signal = sosfiltfilt(filter_params, signal)

discrete_signals = []
discrete_spectrums = []
reconstructed_signals = []
variances = []
snr_values = []

for Dt in Dt_values:
    discrete_signal = np.zeros(n)
    for i in range(0, round(n / Dt)):
        index = i * Dt
        if index < n:
            discrete_signal[index] = filtered_signal[index]
    discrete_signals.append(list(discrete_signal))

    spectrum = fftshift(fft(discrete_signal))
    discrete_spectrums.append(list(np.abs(spectrum)))

    w_filter = F_filter / (Fs / 2)
    filter_params = butter(3, w_filter, 'low', output='sos')
    reconstructed_signal = sosfiltfilt(filter_params, discrete_signal)
    reconstructed_signals.append(list(reconstructed_signal))

    E1 = reconstructed_signal - filtered_signal
    variance_signal = np.var(filtered_signal)
    variance_E1 = np.var(E1)
    snr = variance_signal / variance_E1 if variance_E1 != 0 else np.inf

    variances.append(variance_E1)
    snr_values.append(snr)

# Побудова графіків дискретизованих сигналів
fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(2):
    for j in range(2):
        ax[i][j].plot(time, discrete_signals[s], linewidth=1)
        s += 1
fig.supxlabel("Час (с)", fontsize=14)
fig.supylabel("Амплітуда сигналу", fontsize=14)
fig.suptitle("Сигнал з кроком дискретизації Dt = (2, 4, 8, 16)", fontsize=14)
fig.savefig("./figures/discrete_signals.png", dpi=600)
plt.close(fig)

# Побудова графіків спектрів
fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
freqs = fftshift(fftfreq(n, 1 / Fs))
for i in range(2):
    for j in range(2):
        ax[i][j].plot(freqs, discrete_spectrums[s], linewidth=1)
        s += 1
fig.supxlabel("Частота (Гц)", fontsize=14)
fig.supylabel("Амплітуда спектру", fontsize=14)
fig.suptitle("Спектри сигналів з кроком дискретизації Dt = (2, 4, 8, 16)", fontsize=14)
fig.savefig("./figures/discrete_spectrums.png", dpi=600)
plt.close(fig)

# Побудова графіків відновлених сигналів
fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(2):
    for j in range(2):
        ax[i][j].plot(time, reconstructed_signals[s], linewidth=1)
        ax[i][j].grid(True)
        s += 1
fig.supxlabel("Час (с)", fontsize=14)
fig.supylabel("Амплітуда сигналу", fontsize=14)
fig.suptitle("Відновлені  аналогові сигнали з кроком дискретизації Dt = (2, 4, 8, 16)", fontsize=14)
fig.savefig("./figures/reconstructed_signals.png", dpi=600)
plt.close(fig)

# Графік залежності дисперсії від кроку дискретизації
plt.figure(figsize=(21 / 2.54, 14 / 2.54))
plt.plot(Dt_values, variances, marker='o', linewidth=1)
plt.grid(True)
plt.xlabel("Крок дискретизації", fontsize=14)
plt.ylabel("Дисперсія", fontsize=14)
plt.title("Залежність дисперсії від кроку дискретизації", fontsize=14)
plt.savefig("./figures/variance_vs_dt.png", dpi=600)
plt.close()

# Графік співвідношення сигнал-шум від дисперсії
plt.figure(figsize=(21 / 2.54, 14 / 2.54))
plt.plot(Dt_values, snr_values, marker='o', linewidth=1)
plt.grid(True)
plt.xlabel("Крок дискретизації", fontsize=14)
plt.ylabel("ССШ", fontsize=14)
plt.title("Залежність співвідношення сигнал-шум від кроку дискретизації", fontsize=14)
plt.savefig("./figures/snr_vs_dt.png", dpi=600)
plt.close()
