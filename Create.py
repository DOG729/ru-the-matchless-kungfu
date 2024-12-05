import os
import csv
import sys
import subprocess

# Функция для поиска Unreal Engine по пути
def find_unreal_engine():
    possible_paths = [
        "D:/Epic Games/UE_4.26",
        "C:/Program Files/Epic Games/UE_4.26",
        # Добавьте другие возможные пути, если нужно
    ]
    
    for path in possible_paths:
        if os.path.isdir(path):
            return path
    return None

# Получаем путь к Unreal Engine
unreal_path = find_unreal_engine()
if unreal_path:
    print(f"Unreal Engine найден по пути: {unreal_path}")
else:
    print("Unreal Engine не найден.")
    sys.exit(1)

# Файлы для проверки
FILES_TO_CHECK = [
    "files/Etc/Localization/argument_text_en.csv",
    "files/Etc/Localization/event_dialogue_en.csv",
    "files/Etc/Localization/npc_dialogue_en.csv",
    "files/Etc/Localization/ui_en.csv"
]

def check_csv(file_path):
    errors = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        
        for line_num, row in enumerate(reader, start=2):
            if len(row) != len(header):
                errors.append(f"Ошибка на строке {line_num}: некорректное количество столбцов.")
    
    if errors:
        print(f"Ошибки в файле {file_path}:")
        for error in errors:
            print(error)
        return False  # Возвращаем False, если есть ошибки
    else:
        print(f"Ошибок в файле {file_path} не обнаружено.")
        return True

if __name__ == "__main__":
    all_files_valid = True
    for file in FILES_TO_CHECK:
        if not check_csv(file):
            all_files_valid = False
    if not all_files_valid:
        sys.exit(1)

    print("Обработка завершена.")

    # Получаем текущую директорию
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Путь к файлам .pak и config.txt в текущей папке
    pak_file = os.path.join(current_dir, "HMS_00-WindowsNoEditor_Rus.pak")
    config_file = os.path.join(current_dir, "config.txt")

    # Команда для запуска UnrealPak.exe
    unrealpak_path = os.path.join(unreal_path, "Engine", "Binaries", "Win64", "UnrealPak.exe")
    command = [
        unrealpak_path,
        pak_file,
        f"-Create={config_file}",
        "-compress"
    ]

    try:
        print(f"Выполняем команду: {' '.join(command)}")
        subprocess.run(command, check=True)
        print("Команда выполнена успешно.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")