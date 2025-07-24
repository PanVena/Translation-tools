import os
import sys
import csv
import json
import re

folder = os.path.dirname(os.path.abspath(sys.argv[0]))
csv_files = [f for f in os.listdir(folder) if f.endswith('.csv')]

for csv_file in csv_files:
    csv_path = os.path.join(folder, csv_file)
    txt_name = os.path.splitext(csv_file)[0] + ".txt"
    txt_path = os.path.join(folder, txt_name)

    if not os.path.exists(txt_path):
        print(f"❌ Не знайдено відповідний TXT для {csv_file}")
        continue

    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Помилка читання {txt_path}: {e}")
        continue

    match = re.search(r'm_Script\s*=\s*"(.*)"', content)
    if not match:
        print(f"❌ m_Script не знайдено у {txt_path}")
        continue

    json_str = match.group(1).replace('\\"', '"')
    if not json_str.endswith('}]}'):
        json_str += '}]}'

    try:
        data = json.loads(json_str)
    except Exception as e:
        print(f"❌ JSON помилка в {txt_path}: {e}")
        continue

    # Зчитуємо переклади
    translations = {}
    with open(csv_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row["Key"].strip()
            translated = row["Ukrainian"].strip()
            if translated:
                translations[key] = translated

    # Замінюємо англійський текст
    for item in data.get("Items", []):
        key = item.get("ID", "")
        if key in translations:
            item["English"] = translations[key]

    # Перетворюємо назад у JSON з екрануванням
    new_json = json.dumps(data, ensure_ascii=False).replace('"', '\\"')

    # Замінюємо старий m_Script
    new_content = re.sub(r'(m_Script\s*=\s*")(.+?)(")', rf'\1{new_json}\3', content, flags=re.DOTALL)

    # Записуємо у новий файл
    output_path = os.path.join(folder, f"{os.path.splitext(txt_name)[0]}_оновлено.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ Оновлено English-текст у: {output_path}")
