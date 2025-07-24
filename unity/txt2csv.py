import os
import re
import sys
import json
import csv

folder = os.path.dirname(os.path.abspath(sys.argv[0]))
txt_files = [f for f in os.listdir(folder) if f.endswith('.txt')]

for txt_file in txt_files:
    input_path = os.path.join(folder, txt_file)
    output_path = os.path.join(folder, os.path.splitext(txt_file)[0] + ".csv")

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Помилка при читанні {txt_file}: {e}")
        continue

    match = re.search(r'm_Script\s*=\s*"(.*)"', content)
    if not match:
        print(f"❌ Не знайдено m_Script у {txt_file}")
        continue

    json_str = match.group(1).replace('\\"', '"')
    if not json_str.endswith('}]}'):
        json_str += '}]}'

    try:
        data = json.loads(json_str)
    except Exception as e:
        print(f"❌ JSON помилка у {txt_file}: {e}")
        continue

    items = data.get("Items", [])
    with open(output_path, "w", encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Key", "English", "Ukrainian", "Danish"])
        for item in items:
            key = item.get("ID", "")
            eng = item.get("English", "")
            dan = item.get("Danish", "")
            writer.writerow([key, eng, "", dan])

    print(f"✅ Створено CSV: {output_path}")
