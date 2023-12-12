import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from bs4 import BeautifulSoup
import json
from tkinter import messagebox

def update_import_data(file_path, updated_json_str):
    try:
        # Чтение содержимого HTML файла
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Парсинг HTML с использованием BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Находим первый тэг "import_data"
        import_data_tag = soup.find('import_data')

        if import_data_tag:
            # Обновляем содержимое тэга
            import_data_tag.string = updated_json_str

            # Сохраняем обновленное HTML содержимое в тот же файл
            with open(file_path, 'w', encoding='utf-8') as updated_file:
                updated_file.write(str(soup))

            print(f"Обновленное содержимое записано в файл {file_path}")
        else:
            print("Тэг 'import_data' не найден в HTML файле.")

    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

class DragDropFileField(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)

        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_drop)

        self.create_text(
            150, 50, text="Перетащите файл сюда", font=("Helvetica", 12), fill="gray"
        )

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        delta_x = event.x - self.start_x
        delta_y = event.y - self.start_y
        self.move("all", delta_x, delta_y)
        self.start_x = event.x
        self.start_y = event.y

    def on_release(self, event):
        pass

    def on_drop(self, event):
        # Получение списка файлов, перетащенных на холст
        files = event.data
        self.handle_dropped_files(files)

    def handle_dropped_files(self, files):
        # Обработка перетащенных файлов
        if files:
            # Первый файл из списка
            file_path = files[1:-1]

            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()

                soup = BeautifulSoup(html_content, 'html.parser')
                import_data_tag = soup.find('import_data')

                if import_data_tag:
                    import_data_content = import_data_tag.get_text()
                    import_data_json = json.loads(import_data_content)

                    import_data_json['import_data'] = [row for row in import_data_json['import_data'] if row[2] != 0]

                    # Преобразуем обновленные данные обратно в строку JSON
                    updated_json_str = json.dumps(import_data_json, indent=2, ensure_ascii=False)                    

                    # Записываем обновленные данные в оригинальный файл
                    update_import_data(file_path, "\n"+updated_json_str+"\n")

                    # Показываем окно сообщений с результатом
                    messagebox.showinfo("Результат", updated_json_str)

            except FileNotFoundError:
                messagebox.showerror("Ошибка", f"Файл {file_path} не найден.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")



import tkinter as tk
from tkinter import filedialog

def open_file_dialog(entry):
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    entry.delete(0, tk.END)  # Clear the current entry content
    entry.insert(0, file_path)  # Insert the selected file path

def process_file_path(entry):
    file_path = entry.get()
    # Add your logic to process the file path here
    print(f"Selected File: {file_path}")

def create_interface():
    root = tk.Tk()
    root.title("File Path Entry")

    entry_label = tk.Label(root, text="File Path:")
    entry_label.pack(pady=5)

    entry_var = tk.StringVar()
    entry = tk.Entry(root, textvariable=entry_var, width=40)
    entry.pack(pady=10)

    browse_button = tk.Button(root, text="Browse", command=lambda: open_file_dialog(entry))
    browse_button.pack(pady=5)

    process_button = tk.Button(root, text="Process File", command=lambda: process_file_path(entry))
    process_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_interface()
