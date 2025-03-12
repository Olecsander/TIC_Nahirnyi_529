import os
import random
import string
import collections
import math
import matplotlib.pyplot as plt


def save_to_file(filename, data):
    with open(filename, "a", encoding="utf-8") as file:
        file.write(data + "\n")


def generate_sequence_1(n_sequence=100, n1=11):
    list1 = ["1"] * n1
    list0 = ["0"] * (n_sequence - n1)
    sequence = list1 + list0
    random.shuffle(sequence)
    return "".join(sequence)


def generate_sequence_2(n_sequence=100, surname="Нагірний"):
    list1 = list(surname)
    list0 = ["0"] * (n_sequence - len(list1))
    sequence = list1 + list0
    return "".join(sequence)


def generate_sequence_3(n_sequence=100, surname="Нагірний"):
    list1 = list(surname)
    list0 = ["0"] * (n_sequence - len(list1))
    sequence = list1 + list0
    random.shuffle(sequence)
    return "".join(sequence)


def generate_sequence_4(n_sequence=100, surname="Нагірний", group="529"):
    elements = list(surname) + list(group)
    n_repeats = n_sequence // len(elements)
    remainder = n_sequence % len(elements)
    sequence = (elements * n_repeats) + elements[:remainder]
    return "".join(sequence)


def generate_sequence_5(n_sequence=100):
    alphabet = ['н', 'а', '5', '2', '9']
    Pi = 0.2
    length = Pi * n_sequence
    sequence = alphabet * int(length)
    random.shuffle(sequence)
    return "".join(sequence)


def generate_sequence_6(n_sequence=100, surname="Нагірний", group="529"):
    letters = list(surname[:2])
    digits = list(group)
    n_letters = int(0.7 * n_sequence)
    n_digits = n_sequence - n_letters
    sequence = [random.choice(letters) for _ in range(n_letters)] + [random.choice(digits) for _ in range(n_digits)]
    random.shuffle(sequence)
    return "".join(sequence)


def generate_sequence_7(n_sequence=100):
    elements = list(string.ascii_lowercase) + list(string.digits)
    sequence = [random.choice(elements) for _ in range(n_sequence)]
    return "".join(sequence)


def generate_sequence_8(n_sequence=100):
    return "1" * n_sequence


def calculate_parameters(sequence):
    unique_chars = set(sequence)
    sequence_size = len(sequence)
    return len(unique_chars), sequence_size


def calculate_probabilities(sequence):
    counts = collections.Counter(sequence)
    total = len(sequence)
    probabilities = {char: count / total for char, count in counts.items()}
    return probabilities


def calculate_entropy(probabilities):
    return -sum(p * math.log2(p) for p in probabilities.values() if p > 0)


def main():
    sequences = [
        generate_sequence_1(),
        generate_sequence_2(),
        generate_sequence_3(),
        generate_sequence_4(),
        generate_sequence_5(),
        generate_sequence_6(),
        generate_sequence_7(),
        generate_sequence_8()
    ]

    os.makedirs("LosslessCompression", exist_ok=True)
    results_file = os.path.join("LosslessCompression", "results_sequence.txt")
    sequences_file = os.path.join("LosslessCompression", "sequence.txt")

    results = []

    with open(sequences_file, "w", encoding="utf-8") as file:
        for i, sequence in enumerate(sequences, 1):
            file.write(f"Послідовність {i}: {sequence}\n")

    with open(results_file, "w", encoding="utf-8") as file:
        for i, sequence in enumerate(sequences, 1):
            alphabet_size, size_in_bytes = calculate_parameters(sequence)
            probabilities = calculate_probabilities(sequence)
            entropy = calculate_entropy(probabilities)
            redundancy = math.log2(alphabet_size) - entropy if alphabet_size > 1 else 0

            avg_probability = sum(probabilities.values()) / len(probabilities)
            probability_distribution = "рівна" if all(
                abs(p - avg_probability) < 0.05 for p in probabilities.values()) else "нерівна"

            probability_str = ", ".join(f"{char}-{p:.4f}" for char, p in probabilities.items())

            file.write(f"Послідовність {i}: {sequence}\n")
            file.write(f"Розмір послідовності: {size_in_bytes} byte\n")
            file.write(f"Розмір алфавіту: {alphabet_size}\n")
            file.write(f"Ймовірності появи символів: {probability_str}\n")
            file.write(f"Середнє арифметичне ймовірностей: {avg_probability:.4f}\n")
            file.write(f"Ймовірність розподілу символів: {probability_distribution}\n")
            file.write(f"Ентропія: {entropy:.4f}\n")
            file.write(f"Надмірність джерела: {redundancy:.4f}\n\n")

            results.append([alphabet_size, round(entropy, 2), round(redundancy, 2), probability_distribution])

    # Побудова таблиці
    fig, ax = plt.subplots(figsize=(14 / 1.54, len(sequences) / 1.54))
    plt.title("Характеристики сформованих послідовностей")
    headers = ['Розмір алфавіту', 'Ентропія', 'Надмірність', 'Ймовірність']
    row_labels = [f'Послідовність {i + 1}' for i in range(len(sequences))]

    ax.axis('off')
    table = ax.table(cellText=results, colLabels=headers, rowLabels=row_labels, loc='center', cellLoc='center')
    table.set_fontsize(14)
    table.scale(0.8, 2)

    fig.savefig(os.path.join("LosslessCompression", "Характеристики_сформованих_послідовностей.png"))


if __name__ == "__main__":
    main()
