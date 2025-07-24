import json
import re
import os
import sys

# Папка, де лежить сам скрипт
folder = os.path.dirname(os.path.abspath(sys.argv[0]))

# Знаходимо перший .txt файл, крім самого себе
txt_files = [f for f in os.listdir(folder) if f.endswith('.txt')]

if not txt_files:
    with open(os.path.join(folder, "результат.txt"), "w", encoding="utf-8") as out:
        out.write("❌ У теці немає .txt файлів.")
    sys.exit()

# Беремо перший .txt файл
input_path = os.path.join(folder, txt_files[0])
output_path = os.path.join(folder, f"{os.path.splitext(txt_files[0])[0]}_розкладений.txt")

try:
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
except Exception as e:
    with open(output_path, "w", encoding="utf-8") as out:
        out.write(f"❌ Помилка читання файлу: {e}")
    sys.exit()

# Витягуємо JSON з m_Script
match = re.search(r'm_Script\s*=\s*"(.*)"', content)
if not match:
    with open(output_path, "w", encoding="utf-8") as out:
        out.write("❌ Поле 'm_Script' не знайдено.")
    sys.exit()

json_str = match.group(1).replace('\\"', '"')
if not json_str.endswith('}]}'):
    json_str += '}]}'

# Читаємо JSON
try:
    data = json.loads(json_str)
except json.JSONDecodeError as e:
    with open(output_path, "w", encoding="utf-8") as out:
        out.write(f"❌ JSON помилка: {e}")
    sys.exit()

# Формуємо новий формат
lines = []
for item in data["Items"]:
    lines.append(f'ID: {item["ID"]}')
    for lang, val in item.items():
        if lang != "ID":
            lines.append(f'  {lang}: {val}')
    lines.append("")

# Записуємо результат
with open(output_path, "w", encoding="utf-8") as out:
    out.write("\n".join(lines))

# Відкриваємо результат у Блокноті (опційно)
os.system(f'notepad "{output_path}"')

