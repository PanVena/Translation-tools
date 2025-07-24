import csv
import re

csv_file = 'localization.csv'
txt_file = 'AmericanEnglish-resources.assets-273.txt'
output_file = 'AmericanEnglish-resources.assets-273-updated.txt'

# Зчитуємо ключі і значення (3-й стовпець) з CSV
localization = {}
with open(csv_file, encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) >= 3:
            key = row[0].strip()
            value = row[2].strip()
            localization[key] = value

# Зчитуємо весь текст файлу
with open(txt_file, encoding='utf-8') as f:
    content = f.read()

# Знаходимо всі об’єкти {"Key":"...","Value":"..."}
pattern = re.compile(r'(\{"Key":"(.*?)","Value":"(.*?)"\})', re.DOTALL)

def replacer(match):
    full = match.group(1)
    key = match.group(2)
    old_value = match.group(3)
    if key in localization:
        new_value = localization[key].replace('"', '\\"')
        return f'{{"Key":"{key}","Value":"{new_value}"}}'
    return full

new_content = pattern.sub(replacer, content)

# Записуємо назад у файл
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f'Готово! Результат збережено у {output_file}')
