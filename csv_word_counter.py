import csv
import os
from collections import defaultdict

def count_words(text):
    return len(text.split())

def process_csv_file(filepath):
    word_counts = defaultdict(int)
    headers = []

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames

        for row in reader:
            for header in headers:
                cell = row.get(header, "")
                word_counts[header] += count_words(cell)

    return filepath, headers, word_counts

def main():
    csv_files = []
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.csv'):
                full_path = os.path.join(root, file)
                csv_files.append(full_path)

    if not csv_files:
        print("CSV-файлів не знайдено.")
        return

    global_word_counts = defaultdict(int)
    dir_word_counts = defaultdict(lambda: defaultdict(int))
    file_summaries = []

    for csv_file in csv_files:
        filepath, headers, word_counts = process_csv_file(csv_file)
        relative_path = os.path.relpath(filepath)
        directory = os.path.dirname(relative_path) or "."  # "." якщо в кореневій теці

        # Підсумки
        for header in headers:
            global_word_counts[header] += word_counts[header]
            dir_word_counts[directory][header] += word_counts[header]

        file_summaries.append((relative_path, headers, word_counts))

    with open("загальний_підрахунок_слів.txt", 'w', encoding='utf-8') as f:
        # Загальний підсумок
        f.write("🔷 ЗАГАЛЬНИЙ ПІДСУМОК З УСІХ CSV-ФАЙЛІВ:\n")
        for header in sorted(global_word_counts.keys()):
            f.write(f"{header}: {global_word_counts[header]} слів\n")
        f.write("\n")

        # Підсумки по теках
        f.write("📁 ПІДСУМКИ ПО ТЕКАХ:\n")
        for directory in sorted(dir_word_counts.keys()):
            f.write(f"📂 {directory}:\n")
            for header in sorted(dir_word_counts[directory].keys()):
                f.write(f"  {header}: {dir_word_counts[directory][header]} слів\n")
            f.write("\n")

        # Підсумки по файлах
        f.write("📄 ПІДСУМКИ ПО КОЖНОМУ ФАЙЛУ:\n")
        for filepath, headers, word_counts in file_summaries:
            f.write(f"🗎 {filepath}:\n")
            for header in headers:
                f.write(f"  {header}: {word_counts[header]} слів\n")
            f.write("\n")

    print("✅ Готово! Дані записано в 'загальний_підрахунок_слів.txt'.")

if __name__ == '__main__':
    main()
