from bs4 import BeautifulSoup
def delete_html_tags(input_file_path, output_file_path):
    # Читаємо вміст вхідного файлу
    with open(input_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    # Створюємо об'єкт BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    # Отримуємо текст без HTML тегів
    text = soup.get_text()
    # Записуємо очищений текст у вихідний файл
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(text)

delete_html_tags("C:/Users/vgumenyuk1/Downloads/draft.html", "C:/Users/vgumenyuk1/Downloads/12345.txt" )