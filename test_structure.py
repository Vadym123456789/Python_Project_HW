import os

# Отримуємо поточний шлях
current_path = os.getcwd()
print("Поточний шлях:", current_path)

# Перевіряємо наявність папки templates
templates_path = os.path.join(current_path, 'templates')
if os.path.exists(templates_path):
    print("Папка templates знаходиться в корені проекту")
else:
    print("Папка templates НЕ знаходиться в корені проекту")

# Виводимо повний список файлів і папок
print("\nСтруктура проекту:")
for root, dirs, files in os.walk(current_path):
    level = root.replace(current_path, '').count(os.sep)
    indent = ' ' * 4 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = ' ' * 4 * (level + 1)
    for f in files:
        print(f"{subindent}{f}")