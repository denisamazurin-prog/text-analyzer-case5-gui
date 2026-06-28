import collections
import re
import os
from tkinter import Tk, filedialog, messagebox, Toplevel, BOTH, END
from tkinter.scrolledtext import ScrolledText  # Компонент для скроллинга текста

def read_file_with_encoding(file_path):
    """
    Функция автоматического определения и обработки различных кодировок файла.
    """
    encodings = ['utf-8', 'cp1251', 'latin-1', 'utf-16']
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                return f.read(), enc
        except (UnicodeDecodeError, LookupError):
            continue
    raise UnicodeDecodeError("Не удалось определить кодировку файла.")

def analyze_text(text):
    """Подсчет базовой и продвинутой статистики текста."""
    lines = text.splitlines()
    num_lines = len(lines)
    num_chars = len(text)
    
    # Извлечение слов с помощью регулярного выражения (игнорируя регистр)
    words = re.findall(r'\b\w+\b', text.lower())
    num_words = len(words)
    
    unique_words = set(words)
    num_unique_words = len(unique_words)
    
    # Поиск самых частых слов (топ-5)
    word_counts = collections.Counter(words)
    top_words = word_counts.most_common(5)
    
    return {
        "lines": num_lines,
        "chars": num_chars,
        "words": num_words,
        "unique": num_unique_words,
        "top_words": top_words
    }

def format_statistics(stats, file_path, encoding):
    """Форматирование результатов для вывода."""
    report = [
        f"=== Статистика для файла: {os.path.basename(file_path)} ===",
        f"Успешно определенная кодировка: {encoding}",
        f"Количество строк: {stats['lines']}",
        f"Общее количество символов: {stats['chars']}",
        f"Общее количество слов: {stats['words']}",
        f"Количество уникальных слов: {stats['unique']}",
        "\nТоп-5 самых частых слов:"
    ]
    for word, count in stats['top_words']:
        report.append(f"  - '{word}': {count} раз(а)")
    return "\n".join(report)

def save_report(report, source_file_path):
    """Сохранение отчета в текстовый файл."""
    output_path = os.path.splitext(source_file_path)[0] + "_stats.txt"
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        return output_path
    except Exception as e:
        return None

def show_statistics_window(parent, report_text):
    """Создание отдельного всплывающего окна со статистикой."""
    # Окно верхнего уровня
    window = Toplevel(parent)
    window.title("Результаты анализа")
    window.geometry("550x400")
    window.minsize(400, 300)
    
    # Делаем окно модальным
    window.transient(parent)
    window.grab_set()
    
    # Текстовое поле с полосой прокрутки
    text_area = ScrolledText(window, wrap='word', font=('Courier New', 11))
    text_area.pack(fill=BOTH, expand=True, padx=15, pady=15)
    
    # Добавление контента и защита от случайного редактирования
    text_area.insert(END, report_text)
    text_area.configure(state='disabled')
    
    # Ожидание закрытия окна пользователем
    window.wait_window()

def main():
    root = Tk()
    root.withdraw()
    
    # 1. Выбор файла через GUI
    messagebox.showinfo("Инфо", "Выберите текстовый файл для анализа")
    file_path = filedialog.askopenfilename(
        filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
    )
    
    if not file_path:
        return

    try:
        # 2. Чтение файла с автоподбором кодировки
        text, encoding = read_file_with_encoding(file_path)
        
        # 3. Подсчет статистики
        stats = analyze_text(text)
        
        # 4. Форматирование
        report = format_statistics(stats, file_path, encoding)
        
        # 5. Вывод в консоль
        print(report)
        
        # 6. Сохранение в файл
        output_file = save_report(report, file_path)
        
        # 7. Вывод во всплывающее графическое окно
        show_statistics_window(root, report)
        
        # 8. Уведомление об успешном завершении операции
        if output_file:
            messagebox.showinfo("Успех", f"Анализ завершен успешно!\nОтчет сохранен в:\n{output_file}")
        else:
            messagebox.showwarning("Внимание", "Статистика показана, но не удалось записать файл на диск.")
            
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка при обработке файла:\n{str(e)}")

if __name__ == "__main__":
    main()
