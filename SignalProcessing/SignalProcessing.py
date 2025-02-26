import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import os

# Параметри завдання
n = 500  # Довжина сигналу у відліках
Fs = 1000  # Частота дискретизації
f_max = 23  # Максимальна частота сигналу

t = np.arange(n) / Fs  # Масив часу
original_signal = np.sin(2 * np.pi * f_max * t)  # Гармонічний сигнал

# Фільтрація сигналу (обмеження частоти)
nyquist = Fs / 2
cutoff = f_max / nyquist
b, a = signal.butter(4, cutoff, btype='low')
filtered_signal = signal.filtfilt(b, a, original_signal)

# Підготовка папки для збереження графіків
output_folder = "figures"
os.makedirs(output_folder, exist_ok=True)

# Квантування сигналу
M_values = [4, 16, 64, 256]
quantized_signals = []
variances = []
snr_values = []

for M in [4, 16, 64, 256]:
    delta = (np.max(filtered_signal) - np.min(filtered_signal)) / (M - 1)
    quantized_signal = delta * np.round(filtered_signal / delta)
    quantized_signals.append(quantized_signal)

    quantize_levels = np.arange(np.min(quantized_signal), np.max(quantized_signal) + 1, delta)
    quantize_bit = [format(bits, '0' + str(int(np.log2(M))) + 'b') for bits in range(M)]
    quantize_table = np.column_stack((quantize_levels[:M], quantize_bit[:M]))

    fig, ax = plt.subplots(figsize=(14 / 2.54, M / 2.54))
    table = ax.table(cellText=quantize_table, colLabels=['Значення сигналу', 'Кодова послідовність'], loc='center')
    table.set_fontsize(14)
    table.scale(1, 2)
    ax.axis('off')
    fig.savefig(f"{output_folder}/quantization_table_M{M}.png", dpi=600)
    plt.close(fig)

    bits = []
    for signal_value in quantized_signal:
        for index, value in enumerate(quantize_levels[:M]):
            if np.round(np.abs(signal_value - value), 0) == 0:
                bits.append(quantize_bit[index])
                break

    bits = [int(item) for item in list(''.join(bits))]
    x = np.arange(len(bits))

    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    ax.step(x, bits, linewidth=0.1)
    ax.set_xlabel("Біти")
    ax.set_ylabel("Амплітуда сигналу")
    ax.set_title(f"Кодова послідовність сигналу при кількості рівнів квантування {M}")
    fig.savefig(f"{output_folder}/bit_sequence_M{M}.png", dpi=600)
    plt.close(fig)

    variance = np.var(filtered_signal - quantized_signal)
    variances.append(variance)
    snr = 10 * np.log10(np.var(filtered_signal) / variance)
    snr_values.append(snr)

# Побудова графіка цифрових сигналів з різними рівнями квантування
fig, axes = plt.subplots(4, 1, figsize=(21 / 2.54, 14 / 2.54), sharex=True)

for i, M in enumerate(M_values):
    axes[i].plot(t, quantized_signals[i], label=f"M = {M}", color=f"C{i}")
    axes[i].set_ylabel("Амплітуда")
    axes[i].legend()
    axes[i].grid()

axes[-1].set_xlabel("Час (с)")
fig.suptitle("Цифрові сигнали з рівнями квантування (4, 16, 64, 256)", fontsize=14)

plt.tight_layout()
plt.savefig(f"{output_folder}/quantized_signals.png", dpi=600)
plt.close(fig)

fig, ax = plt.subplots()
ax.plot([4, 16, 64, 256], variances, marker='o')
ax.set_xlabel("Кількість рівнів квантування")
ax.set_ylabel("Дисперсія")
ax.set_title("Залежність дисперсії від кількості рівнів квантування")
fig.savefig(f"{output_folder}/variance_vs_M.png", dpi=600)
plt.close(fig)

fig, ax = plt.subplots()
ax.plot([4, 16, 64, 256], snr_values, marker='o')
ax.set_xlabel("Кількість рівнів квантування")
ax.set_ylabel("ССШ")
ax.set_title("Залежність співвідношення сигнал-шум від кількості рівнів квантування")
fig.savefig(f"{output_folder}/snr_vs_M.png", dpi=600)
plt.close(fig)
