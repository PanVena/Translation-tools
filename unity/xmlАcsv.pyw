import os
import xml.etree.ElementTree as ET
import csv
from collections import defaultdict

def build_key(event_name, idx, duration, line_name):
    line_name_str = line_name if line_name else "None"
    return f"{event_name};{idx};{duration};{line_name_str}"

def parse_key(key):
    event_name, idx, duration, line_name = key.split(';')
    return duration, line_name, event_name, int(idx)

def convert_all_xml_to_csv():
    for filename in os.listdir():
        if filename.endswith(".xml"):
            xml_to_csv(filename)

def xml_to_csv(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    rows = []
    for log in root.findall(".//AudioLog"):
        event_name = log.attrib.get('Name', 'UnknownEvent')
        lines = log.find('MyLines')
        if lines is not None:
            for idx, line in enumerate(lines.findall('Line'), start=1):
                text = line.findtext('Text', '').strip()
                duration = line.findtext('Duration', '0.0').strip()
                comment = line.findtext('Comment', '').strip()
                line_name = line.attrib.get('Name', '')

                key = build_key(event_name, idx, duration, line_name)
                rows.append([key, text, "", comment])  # Key, English, Translation (empty), Comment

    csv_file = xml_file.replace(".xml", ".csv")
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Key', 'English', 'Translation', 'Comment'])
        writer.writerows(rows)
    print(f"[✓] CSV written: {csv_file}")

def convert_all_csv_to_xml():
    for filename in os.listdir():
        if filename.endswith(".csv"):
            csv_to_xml(filename)

def csv_to_xml(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        lines = list(reader)

    grouped = defaultdict(list)
    for row in lines:
        key = row['Key']
        duration, line_name, event_name, idx = parse_key(key)
        grouped[event_name].append((idx, row, duration, line_name))

    subtitle_collection = ET.Element('SubtitleCollection')
    subtitle_groups = ET.SubElement(subtitle_collection, 'SubtitleGroups')

    for event_name, rows in grouped.items():
        audio_log = ET.SubElement(subtitle_groups, 'AudioLog', Name=event_name)
        my_lines = ET.SubElement(audio_log, 'MyLines')

        # Сортуємо рядки за індексом, щоб зберегти порядок
        for idx, row, duration, line_name in sorted(rows, key=lambda x: x[0]):
            line_elem = ET.SubElement(my_lines, 'Line', Name=line_name if line_name != "None" else "")
            ET.SubElement(line_elem, 'Text').text = row['Translation'] or row['English']
            ET.SubElement(line_elem, 'Duration').text = duration
            ET.SubElement(line_elem, 'Comment').text = row['Comment']

    out_file = csv_file.replace(".csv", "_reconstructed.xml")
    tree = ET.ElementTree(subtitle_collection)
    tree.write(out_file, encoding='utf-8', xml_declaration=True)
    print(f"[✓] XML reconstructed with all AudioLogs: {out_file}")

def main():
    import sys

    if len(sys.argv) > 1:
        import argparse
        parser = argparse.ArgumentParser(description="Convert XML <-> CSV for AudioLogs")
        parser.add_argument('--to-csv', action='store_true', help="Convert all XML files in folder to CSV")
        parser.add_argument('--to-xml', action='store_true', help="Convert all CSV files in folder to XML")

        args = parser.parse_args()

        if args.to_csv:
            convert_all_xml_to_csv()
        elif args.to_xml:
            convert_all_csv_to_xml()
        else:
            print("Use --to-csv or --to-xml")
    else:
        print("Виберіть дію:")
        print("1. Конвертувати всі XML у CSV")
        print("2. Конвертувати всі CSV у XML")
        choice = input("Введіть номер дії (1 або 2): ").strip()
        if choice == '1':
            convert_all_xml_to_csv()
        elif choice == '2':
            convert_all_csv_to_xml()
        else:
            print("Невірний вибір. Вихід.")


if __name__ == "__main__":
    main()
